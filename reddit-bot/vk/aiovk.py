

async def test(data):
    with open("DASH_96.mp4", "rb") as mp4_file:
        data.add_field("mp4", mp4_file)

async def encoding_medias(medias: list[Media]) -> MultipartEncoder:
    images = {}
    for media in medias:
        images['file1'] = (
                "DASH_96.mp4",
                open(f"DASH_96.mp4", "rb"),
                f"video/mp4"
                )
    return MultipartEncoder(fields=images)
    

async def upload_photos_to_server(url: str, medias:  list[Media]):
    """Передает фотографии на сервер по ссылке,
    полученной методом get_wall_upload_server."""
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        await test(data)
        response = await session.post(
                url=url,
                data=data,
                headers={"multipart/form-data"})
        return await response.json()
