from connect import DB


async def reset_streak(context):
    db = DB()
    db.reset_streak()
    