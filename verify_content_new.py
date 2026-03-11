import asyncio
import httpx
import os

async def verify_content():
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        # 1. Verify /content listing page
        print("Verifying /content...")
        res = await client.get(f"{base_url}/content")
        assert res.status_code == 200
        content = res.text
        assert "Cultural Relevance" in content
        assert "Scalable Design" in content
        assert "Reference Model Hub" in content
        assert "/content/cultural-relevance" in content
        print("Listing page OK.")

        # 2. Verify Cultural Relevance detail page
        print("Verifying Cultural Relevance detail...")
        res = await client.get(f"{base_url}/content/cultural-relevance")
        assert res.status_code == 200
        content = res.text
        assert "Cultural Relevance" in content
        assert "In the heart of Africa" in content
        # Check for text-justify
        assert "text-justify" in content
        # Check for whitespace-pre-line
        assert "whitespace-pre-line" in content
        print("Cultural Relevance detail OK.")

        # 3. Verify Scalable Design detail page
        print("Verifying Scalable Design detail...")
        res = await client.get(f"{base_url}/content/scalable-design")
        assert res.status_code == 200
        content = res.text
        assert "Scalable Design" in content
        assert "Scalability" in content
        print("Scalable Design detail OK.")

        # 4. Verify Reference Model Hub detail page
        print("Verifying Reference Model Hub detail...")
        res = await client.get(f"{base_url}/content/reference-model-hub")
        assert res.status_code == 200
        content = res.text
        assert "Reference Model Hub" in content
        assert "Reference Model Hub" in content
        print("Reference Model Hub detail OK.")

if __name__ == "__main__":
    asyncio.run(verify_content())
