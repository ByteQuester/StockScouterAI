from streamlit_elements import mui

from .dashboard import Dashboard


class Card(Dashboard.Item):

    DEFAULT_CONTENT = ("This impressive app is a perfect and fun way to learn "
                       "together. New features are underway.")

    def __call__(self, content):
        with mui.Card(key=self._key,
                      sx={
                          "display": "flex",
                          "flexDirection": "column",
                          "borderRadius": 3,
                          "overflow": "hidden"
                      },
                      elevation=1):
            mui.CardHeader(
                title="Investment Bot",
                subheader="Jan 12, 2024",
                avatar=mui.Avatar("R", sx={"bgcolor": "red"}),
                action=mui.IconButton(mui.icon.MoreVert),
                className=self._draggable_class,
            )
            mui.CardMedia(
                component="img",
                height=194,
                #image="gallery/interface/misc/demo.jpeg",
                alt="Gallery Bot",
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(content)

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)
