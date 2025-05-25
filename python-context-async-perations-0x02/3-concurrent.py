import asyncio
import aiosqlite 

async def async_fetch_users():
    """Fetch all users from the database."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users


async def async_fetch_older_users():
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users


async def fetch_concurrently():
    """Execute both fetch operations concurrently."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    all_users, older_users = results
    print(f"All users: {all_users}")
    print(f"Users older than 40: {older_users}")
    
    return results


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())