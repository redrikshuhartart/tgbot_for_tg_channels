# tgbot_for_tg_channels
Telegram bot, which allows you to create posts in the target channel containing a button, audio, video or photo material.

The idea of a particular bot is as follows. You want to attract subscribers to the channels you need and hold a prize draw.

You give the bot administrator rights in the telegram channel in which you want to post a prize draw, as well as in those where you want to attract subscribers.

Then you upload to the bot the media content that you want to attach to the message. Specify the text of the message signature, as well as the text of the button that will appear under your post.

In the current implementation of the bot, this button checks whether the user is subscribed to the channels that you specify as those where you want to attract subscribers and if the result is positive, adds the user to the table of participants in the draw.

At the time you need, you can select a winner in the bot menu via the button that extracts a random user from the database.
