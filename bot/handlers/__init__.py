from .basic_commands import bot, dp
from .add_new_citation import bot, dp
from .send_citation import bot, dp
from .inc_dec_likes_dislikes import bot, dp
from .settings import bot, dp
from .delete_citation import dp
from .error_catcher import bot, dp

__all__ = ["dp", "bot"]