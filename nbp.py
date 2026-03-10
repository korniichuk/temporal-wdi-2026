from temporalio import workflow
from temporalio.exceptions import ApplicationError

with workflow.unsafe.imports_passed_through():
    import httpx


async def get_usd_rate() -> str:
    url = "http://api.nbp.pl/api/exchangerates/rates/c/usd/"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code >= 400:
            raise ApplicationError(
                f"HTTP Error {r.status_code}",
                non_retryable=r.status_code < 500,  # retry 5xx but not 4xx
            )
        data = r.json()
        buy = data['rates'][0]['bid']
        sell = data['rates'][0]['ask']
        effective_date = data['rates'][0]['effectiveDate']
        text = f"USD buy: {buy}\nUSD sell: {sell}\n{effective_date}"
    return text
