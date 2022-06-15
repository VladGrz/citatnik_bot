from .add_new_citation import dp
from .send_citation import dp
from .inc_dec_likes_dislikes import dp
from .settings import dp
from .delete_citation import dp
from .error_catcher import bot, dp
from .change_sort_type import dp
from .basic_commands import dp

__all__ = ["dp", "bot"]
