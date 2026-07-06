import json
import os
import traceback
## authorizer
import authorizer
## notification
import notification

""" Aftership main handler """

def aftership(event, context):
    
    try:
        print(event)
        body = event["body"]
        if isinstance(body, str):
            vbody = body
            body = json.loads(body)
        print(body)
        for k in body:
            print(k)

        signature = str(headers["Aftership-Hmac-Sha256"])
        # passing vbody which is the raw body of the message (str).  Will not work
        # with json.dumps()
        result = authorizer.verify_signature(vbody, signature, str(os.environ["webhook_secret"]))
        if result:
            print("authorized")
        else:
            print("unauthorized")
            # Return a 401 Unauthorized response
            body = {"message": "Unauthorized"}
            response = {"statusCode": 401, "body": json.dumps(body)}
            return response

        msg = body.get("msg", {})
        latest_est = msg.get("latest_estimated_delivery")
        expected_delivery = msg.get("expected_delivery")
        latest_est_date_time = latest_est.get("datetime") if isinstance(latest_est, dict) else expected_delivery

        first_est = msg.get("first_estimated_delivery")
        first_est_date_time = first_est.get("datetime") if isinstance(first_est, dict) else None
        expected_delivery_date_time = latest_est_date_time or first_est_date_time
       
        checkpoints = msg.get("checkpoints") or []
        if checkpoints:
            last_checkpoint = checkpoints[-1]
            status = last_checkpoint.get("subtag_message")
            carrier = last_checkpoint.get("slug")
            checkpoint_time = last_checkpoint.get("checkpoint_time")
        else:
            status = msg.get("tag")
            carrier = msg.get("slug")  # fallback to top-level slug
            checkpoint_time = None

        headers = event.get("headers")
        
        request_data = {
            "event": body.get("event"),
            "event_id": body.get("event_id"),
            "is_tracking_first_tag": bool(body.get("is_tracking_first_tag")),
            "order_number": msg.get("order_number"),
            "id": msg.get("id"),
            "status": status,
            "checkpoint_time": checkpoint_time,
            "carrier_name": carrier,
            "tracking_number": msg.get("tracking_number"),
            "courier_tracking_link": msg.get("courier_tracking_link"),-
            "first_est_date_time": first_est_date_time,
            "expected_delivery_date_time": expected_delivery_date_time,
            "pickup_note":  msg.get("pickup_note"),
            "pickup_location": msg.get("pickup_location")
        }

        print(request_data)
        notification.slackNotify(request_data)

        body = {"message": "Message Received"}
        response = {"statusCode": 200, "body": json.dumps(body)}
        return response
    except Exception as error:
        body = {"message": "Server Error"}
        print("An exception occurred:", error)
        traceback.print_exc()
        tb_str = traceback.format_exc()
        notification.slackErrorNotify(str(error), tb_str)
        response = {"statusCode": 200, "body": json.dumps(body)}
        return response