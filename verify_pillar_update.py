import httpx
import asyncio
import sys

async def verify():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        try:
            response = await client.get("/pillars/01")
            if response.status_code != 200:
                print(f"Error: Status code {response.status_code}")
                sys.exit(1)

            content = response.text

            # Check for new content strings (considering HTML entities)
            expected_strings = [
                "In the realm of African-Centered AI Research, NAIRA is pioneering a paradigm shift",
                "Morocco&#39;s Berber (Amazigh) communities",
                "Zimbabwe&#39;s Shona heritage",
                "South Africa&#39;s Zulu ubuntu philosophy",
                "Central Africa&#39;s Bantu groups",
                "whitespace-pre-line"
            ]

            for s in expected_strings:
                if s not in content:
                    print(f"Error: Expected string '{s}' not found in response")
                    sys.exit(1)

            print("Verification successful!")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(verify())
