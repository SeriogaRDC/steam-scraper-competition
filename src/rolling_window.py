"""
Fixed Rolling Window Rate Limiter Implementation.
Addresses common issues with time-based rate limiting in competitive programming.
"""

import time
from collections import deque
from threading import Lock
from typing import Optional


class RollingWindow:
    """
    Thread-safe rolling window rate limiter with proper time handling.
    
    Fixes common issues:
    - Proper time window management
    - Thread safety for concurrent access
    - Memory efficient with automatic cleanup
    - Accurate rate limiting without drift
    """
    
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize rolling window rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
        """
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
            
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()  # Store request timestamps
        self.lock = Lock()  # Thread safety
    
    def can_make_request(self) -> bool:
        """
        Check if a request can be made without exceeding the rate limit.
        
        Returns:
            True if request is allowed, False otherwise
        """
        with self.lock:
            self._cleanup_old_requests()
            return len(self.requests) < self.max_requests
    
    def make_request(self) -> bool:
        """
        Attempt to make a request, recording it if allowed.
        
        Returns:
            True if request was allowed and recorded, False otherwise
        """
        with self.lock:
            self._cleanup_old_requests()
            
            if len(self.requests) < self.max_requests:
                self.requests.append(time.time())
                return True
            return False
    
    def wait_if_needed(self) -> Optional[float]:
        """
        Calculate how long to wait before the next request is allowed.
        
        Returns:
            Number of seconds to wait, or None if no wait is needed
        """
        with self.lock:
            self._cleanup_old_requests()
            
            if len(self.requests) < self.max_requests:
                return None
            
            # Calculate when the oldest request will expire
            oldest_request = self.requests[0]
            wait_time = (oldest_request + self.window_seconds) - time.time()
            return max(0, wait_time)
    
    def wait_and_make_request(self) -> float:
        """
        Wait if necessary and then make a request.
        
        Returns:
            Time waited in seconds
        """
        wait_time = self.wait_if_needed()
        if wait_time and wait_time > 0:
            time.sleep(wait_time)
        
        # Make the request (should always succeed after waiting)
        success = self.make_request()
        if not success:
            # This shouldn't happen, but handle gracefully
            raise RuntimeError("Failed to make request after waiting")
        
        return wait_time or 0
    
    def _cleanup_old_requests(self):
        """Remove requests that are outside the current window."""
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds
        
        # Remove old requests from the left of the deque
        while self.requests and self.requests[0] <= cutoff_time:
            self.requests.popleft()
    
    def get_current_usage(self) -> dict:
        """
        Get current rate limiter statistics.
        
        Returns:
            Dictionary with usage statistics
        """
        with self.lock:
            self._cleanup_old_requests()
            return {
                'current_requests': len(self.requests),
                'max_requests': self.max_requests,
                'window_seconds': self.window_seconds,
                'usage_percentage': (len(self.requests) / self.max_requests) * 100,
                'requests_remaining': self.max_requests - len(self.requests),
                'window_reset_in': self._time_until_reset()
            }
    
    def _time_until_reset(self) -> Optional[float]:
        """Calculate time until the window resets (oldest request expires)."""
        if not self.requests:
            return None
        
        oldest_request = self.requests[0]
        reset_time = oldest_request + self.window_seconds
        return max(0, reset_time - time.time())
    
    def reset(self):
        """Clear all recorded requests (useful for testing)."""
        with self.lock:
            self.requests.clear()
    
    def __str__(self) -> str:
        """String representation of the rate limiter."""
        stats = self.get_current_usage()
        return (f"RollingWindow({stats['current_requests']}/{self.max_requests} "
                f"requests in {self.window_seconds}s window)")
    
    def __repr__(self) -> str:
        """Detailed representation of the rate limiter."""
        return (f"RollingWindow(max_requests={self.max_requests}, "
                f"window_seconds={self.window_seconds}, "
                f"current_requests={len(self.requests)})")


class AdaptiveRollingWindow(RollingWindow):
    """
    Enhanced rolling window that adapts to server responses.
    Useful for handling dynamic rate limits or server load.
    """
    
    def __init__(self, max_requests: int, window_seconds: int, 
                 adaptive_factor: float = 0.8):
        """
        Initialize adaptive rolling window.
        
        Args:
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
            adaptive_factor: Factor to reduce rate when encountering limits (0.0-1.0)
        """
        super().__init__(max_requests, window_seconds)
        self.original_max_requests = max_requests
        self.adaptive_factor = max(0.1, min(1.0, adaptive_factor))
        self.consecutive_limits = 0
        self.consecutive_success = 0
    
    def handle_rate_limit_response(self):
        """Call this when receiving a rate limit response from the server."""
        with self.lock:
            self.consecutive_limits += 1
            self.consecutive_success = 0
            
            # Reduce the effective rate limit
            if self.consecutive_limits >= 3:
                new_max = int(self.max_requests * self.adaptive_factor)
                self.max_requests = max(1, new_max)
    
    def handle_successful_response(self):
        """Call this when receiving a successful response from the server."""
        with self.lock:
            self.consecutive_success += 1
            self.consecutive_limits = 0
            
            # Gradually increase the rate limit back to original
            if self.consecutive_success >= 10 and self.max_requests < self.original_max_requests:
                self.max_requests = min(
                    self.original_max_requests,
                    int(self.max_requests * 1.1)
                )
