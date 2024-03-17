# Play python

## Getting started

```sh
curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry run test
```

## Async generator with FastAPI middleware

### Issue

- looks like ContextMiddleware intercepts each SSE response => bind each 2 yielded values

```python
app.add_middleware(
    ContextMiddleware,
    plugins={ForwardedForPlugin()}
)
```

- If there are only sync logics on async iterator (no await), cannot get yielded value until encounter next await
  - In this case, looks like ContextMiddleware await on each 2 yields
  - Without ContextMiddleware, it yields all values at once after executing all iterations

```
tests/test_main.py::test_stream_err

>>> rigt before yield: 1 / 5 (20.0%)
>>> rigt before yield: 2 / 5 (40.0%)
1 / 5 (20.0%)
2 / 5 (40.0%)
>>> rigt before yield: 3 / 5 (60.0%)
>>> rigt before yield: 4 / 5 (80.0%)
3 / 5 (60.0%)
4 / 5 (80.0%)
>>> rigt before yield: 5 / 5 (100.0%)
5 / 5 (100.0%)
```

### Solution

- Workaround: do `await asyncio.sleep(0.01)` right after yield
  - FastAPI executes `def` route on external threadpool(new thread, non-blocking) but `async def` on internal threadpool(blocking)
  - Using `await`, it returns the control to event loop so that it can execute another task
- Direct: split sync and async logics, so that use sync generator

### Consideration

- What if there should be async logics in generator? Any other problems?
- With sync generator, can it handle multiple calls?
  - if not, we should use gunicorn and multiple workers
