if isDepartureDone:
    return {
        "status": "error",
        "message": "Invalid request! Today already departure",
        "data": data
    }
else:
    currentActiveEvent = await self.eventModel.getData(data, "getCurrentActiveEvent")

    if currentActiveEvent['status'] == "success":
        isArrivalRequest = await self.Event.isArrivalRequest(data.event_name_id)
        if isArrivalRequest == True and data.status == 2:
            return {
                "status": "error",
                "message": "Invalid request! The arrival return request does not exist.",
                "data": data
            }
        else:
            currentActiveEventData = currentActiveEvent['data'][0]

            current_active_event_db_action_date = currentActiveEventData[
                'event_start_user_utc_date_time']
            user_utc_current_date = await self.Frz.getDateTimeByUTC(int(utcDbData['time_zone']), True)
            isDayOver = await self.Event.isDayOver(current_active_event_db_action_date, user_utc_current_date)

            lunchBreakEventId = await self.Event.getLunchBreakEventId()
            checkLunchBreakParams = {
                "user_id": data.user_id,
                "event_name_id": lunchBreakEventId,
                "event_start_date_time": currentActiveEventData['event_start_date_time'],
                "event_start_user_utc_date_time": currentActiveEventData[
                    'event_start_user_utc_date_time'],
            }
            checkLunchBreakParamsObject = self.DOT.convert_to_dotdict(checkLunchBreakParams)
            isLunchBreakDataInfo = await self.eventModel.getData(checkLunchBreakParamsObject, "isLunchBreakDone")

            if isDayOver:
                ## update old/current event
                extra_data = {
                    "lunch_break": await self.Event.isLunchBreakDone(
                        isLunchBreakDataInfo["status"])
                }

                event_update_data = await self.Event.eventStatusDayOver(currentActiveEventData['event_name_id'],
                                                                        extra_data)

                update_event_object = {
                    "event_action_type": event_update_data['event_action_type'],
                    "is_missing_event": event_update_data['is_missing_event'],
                    "event_penalty_id": event_update_data['event_penalty_id'],
                    "missing_event_information": event_update_data[
                        'missing_event_information'],
                    "status": 2,
                    "comments": "Auto closed day event user UTC date is " + user_utc_current_date,
                    "event_end_date_time": await self.Frz.getCurrentDateTime(),
                    "event_end_user_utc_date_time": user_utc_current_date,

                    "event_end_ip": data.user_ip,
                    "id": currentActiveEventData['id']
                }

                pendingEventUpdateResult = await self.eventModel.updateEvent(
                    update_event_object)
                if pendingEventUpdateResult == "success":

                    # create new event

                    if data.status == 2:
                        # 2 is return request so , here not allowed
                        return {
                            "status": "error",
                            "message": "Invalid request! The day is over. Please make a new arrival request.",
                            "data": data
                        }
                    else:

                        event_start_date_time = await self.Frz.getCurrentDateTime()
                        isArrivalToday = await self.eventModel.isArrivalToday(data.user_id, user_utc_current_date)
                        isArrivalRequest = await self.Event.isArrivalRequest(
                            data.event_name_id)
                        if isArrivalToday == False and isArrivalRequest == False:
                            # not exist arrival but request other that impossible
                            return {
                                "status": "error",
                                "message": "Invalid request! The day is over. Please make a new arrival request.",
                                "data": data
                            }
                        else:

                            # in means only allow arrival request then it will work
                            action_user_utc_date_time = await self.Frz.getDateTimeByUTC(
                                int(utcDbData['time_zone']))
                            optionNalObj = {
                                "action_user_utc_date_time": action_user_utc_date_time
                            }
                            insertData = await self.eventModel.insertData(data,
                                                                          optionNalObj,
                                                                          "addEvent")
                            if insertData['status'] == "success":
                                eData = {
                                    "action_user_utc_date_time": action_user_utc_date_time,
                                    "request_data": data
                                }
                                return self.mgsLib.insertMessage("success", False, eData)
                            else:
                                return self.mgsLib.insertMessage(insertData['status'],
                                                                 False, data)



                else:
                    return self.mgsLib.updateMessage("error", False, data)
            else:

                # return status event
                if currentActiveEventData['event_name_id'] == data.event_name_id and \
                        currentActiveEventData['status'] == data.status:
                    return {
                        "status": "success",
                        "message": "Your request is already active. No further action is required.",
                        "data": data
                    }
                else:






    else:

        # create new fresh event
        action_user_utc_date_time = await self.Frz.getDateTimeByUTC(
            int(utcDbData['time_zone']),
            True)
        optionNalObj = {
            "action_user_utc_date_time": action_user_utc_date_time
        }
        event_start_date_time = await self.Frz.getCurrentDateTime()
        isArrivalToday = await self.eventModel.isArrivalToday(data.user_id, action_user_utc_date_time)
        isArrivalRequest = await self.Event.isArrivalRequest(data.event_name_id)
        if isArrivalToday == False and isArrivalRequest == False:
            # not exist arrival but request other that impossible
            return {
                "status": "error",
                "message": "Invalid request! Please make first arrival  request.",
                "data": data
            }
        elif isArrivalToday == False and isArrivalRequest == True and data.status == 2:
            # not exist arrival but request other that impossible
            return {
                "status": "error",
                "message": "Invalid request! Please make first arrival  request.",
                "data": data
            }
        else:
            if data.status == 2:
                # 2 is return request so , here not allowed
                return {
                    "status": "error",
                    "message": "Invalid request!",
                    "data": data
                }
            else:

                insertData = await self.eventModel.insertData(data, optionNalObj,
                                                              "addEvent")
                if insertData['status'] == "success":
                    eData = {
                        "action_user_utc_date_time": action_user_utc_date_time,
                        "request_data": data
                    }
                    return self.mgsLib.insertMessage("success", False, eData)
                else:
                    return self.mgsLib.insertMessage(insertData['status'], False, data)