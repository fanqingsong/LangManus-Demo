"""Decorator utilities for LangManus Demo tools."""

import functools
import time
import logging
from typing import Any, Callable, Dict, Optional
import threading

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0, exponential_backoff: bool = True):
    """Decorator to retry function execution on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        exponential_backoff: Whether to use exponential backoff
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}, retrying in {current_delay}s")
                        time.sleep(current_delay)
                        if exponential_backoff:
                            current_delay *= 2
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            
            # If we get here, all attempts failed
            raise last_exception
        
        return wrapper
    return decorator


def timeout(seconds: float):
    """Decorator to add timeout to function execution.
    
    Args:
        seconds: Timeout in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(seconds)
            
            if thread.is_alive():
                logger.error(f"Function {func.__name__} timed out after {seconds} seconds")
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        
        return wrapper
    return decorator


def log_execution(level: int = logging.INFO):
    """Decorator to log function execution.
    
    Args:
        level: Logging level
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            logger.log(level, f"Starting execution of {func_name}")
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.log(level, f"Completed {func_name} in {execution_time:.2f} seconds")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Failed {func_name} after {execution_time:.2f} seconds: {e}")
                raise
        
        return wrapper
    return decorator


def cache_result(ttl: Optional[float] = None):
    """Decorator to cache function results.
    
    Args:
        ttl: Time to live for cache entries in seconds (None for no expiration)
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        cache_times = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = str(args) + str(sorted(kwargs.items()))
            
            # Check if result is cached and not expired
            if key in cache:
                if ttl is None or (time.time() - cache_times[key]) < ttl:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cache[key]
                else:
                    # Remove expired entry
                    del cache[key]
                    del cache_times[key]
            
            # Execute function and cache result
            logger.debug(f"Cache miss for {func.__name__}, executing function")
            result = func(*args, **kwargs)
            cache[key] = result
            cache_times[key] = time.time()
            
            return result
        
        return wrapper
    return decorator


def validate_args(**validators):
    """Decorator to validate function arguments.
    
    Args:
        **validators: Dictionary of argument names to validation functions
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate arguments
            for arg_name, validator in validators.items():
                if arg_name in bound_args.arguments:
                    value = bound_args.arguments[arg_name]
                    try:
                        if not validator(value):
                            raise ValueError(f"Validation failed for argument '{arg_name}' with value {value}")
                    except Exception as e:
                        raise ValueError(f"Validation error for argument '{arg_name}': {e}")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def safe_execute(default_return: Any = None, log_errors: bool = True):
    """Decorator to safely execute functions with error handling.
    
    Args:
        default_return: Default value to return on error
        log_errors: Whether to log errors
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {e}")
                return default_return
        
        return wrapper
    return decorator


def rate_limit(calls_per_second: float):
    """Decorator to rate limit function calls.
    
    Args:
        calls_per_second: Maximum calls per second
    """
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        min_interval = 1.0 / calls_per_second
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            last_called[0] = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
