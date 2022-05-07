from data.sqllite3_bd import fill_in_data_bd


class History_data():
    def __init__(self):
        self.message = {}
        self.stick = {}
        self.file = {}
        self.video = {}

    async def set_message(self, nam_day, message):
        self.message[nam_day] = message

    async def set_stick(self, nam_day, stick):
        self.stick[nam_day] = stick

    async def set_file(self, nam_day, file):
        self.file[nam_day] = file

    async def set_video(self, nam_day, video):
        self.video[nam_day] = video

    async def fill_in_data(self):
        data = await fill_in_data_bd()
        for day, photo, stiker, text, video in data:
            await self.set_message(day, text)
            await self.set_file(day, photo)
            await self.set_stick(day, stiker)
            await self.set_video(day, video)

