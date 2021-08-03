from discord import Message
from discord.ext.commands import Bot, Cog

from check_words import check_words as cw


class Checker(Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener(name='on_message')
    async def word_checker(self, message: Message) -> None:
        if message.author.bot:  # botであれば弾く
            return

        else:  # ユーザーによる投稿の場合

            before_text: str = message.content  # 触る前の投稿を格納
            check_text: str = message.content  # 上と同じテキストを格納
            check_list: list = []  # あとで置き換えるときの変換後ワードが格納されたリスト

            for i, one_dic in enumerate(cw.check_words.items()):  # one_dicは単語と読みのタプルです。添字は0と1
                check_text: str = check_text.replace(one_dic[0], '{' + str(i) + '}')
                check_list.append(one_dic[1])  # 変換が発生した順番に変換後ワードリストに追加

            if before_text != check_text:  # 最初の投稿から変換が行われた場合
                check_text: str = check_text.format(*check_list)  # 変換後ワードリストを引数に
                await message.channel.send(check_text)  # 送信チャンネルに変換御テキストを送信

            else:  # 変換が行われていない場合
                return  # 何もしない


def setup(bot: Bot) -> None:
    bot.add_cog(Checker(bot))
