import requests
import json
from plugins import register, Plugin, Event, logger, Reply, ReplyType


@register
class DY(Plugin):
    name = "dy"

    def did_receive_message(self, event: Event):
        pass

    def will_generate_reply(self, event: Event):
        query = event.context.query
        if self.config.get("command") in query:
            #rawmsg = event.message._raw_msg
            #print(rawmsg)
            dyurl = query
            event.reply = self.reply(dyurl)
            event.bypass()
            
    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def help(self, **kwargs) -> str:
        return "Use the command you set with command field in the config to get a wonderful video"

    def reply(self, dyurl) -> Reply:
        reply = Reply(ReplyType.TEXT, "Failed to get dy videos")
        try:
            print(dyurl)
            response = requests.post(
                "https://getdytkrealurlapi.9em.org",
                headers={'Content-Type': 'application/json'},
                data=json.dumps({"url": dyurl})  # 示例URL
            )
            if response.status_code == 200:
                rdata = response.json()
                if rdata.get("message") == "success":
                    videos_url = rdata.get("finalUrl")
                    #print(videos_url)
                    if len(videos_url) > 0:
                        reply = Reply(ReplyType.VIDEO, f"{videos_url}")
                else:
                    logger.error("Error: Wrong URL")
            else:
                logger.error(f"Abnormal site status, request: {response.status_code}")
        except Exception as e:
            logger.error(f"Video api call error: {e}")
        return reply
