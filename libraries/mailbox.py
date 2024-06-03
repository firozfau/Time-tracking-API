import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime,timedelta

class Mailbox:

    def __init__(self):
        pass

    async def mail_configuration(self):
        return {
            'host': 'smtp.gmail.com',
            'port': 587,
            'secure': False,
            'requireTLS': True,
            'auth': {
                'name': 'Time Tracking System',
                'user': 'abcdefgh@gmail.com',
                'pass': 'abcdefghnopass'
            }
        }


    async def dateFormate(self,input_date):
        # Parse input date string
        date_time_obj = datetime.strptime(input_date, '%Y-%m-%d %I:%M:%S %p')
        # Extract date part
        date_str = date_time_obj.strftime('%Y-%m-%d')

        return date_str
    async def daYofDateFormate(self,input_date):
        # Parse input date string
        date_time_obj = datetime.strptime(input_date, '%Y-%m-%d %I:%M:%S %p')

        # Format date as 'Wednesday, 29 May 2024'
        formatted_date = date_time_obj.strftime('%A, %d %B %Y')

        return formatted_date

    async def subtractOneDay(self,input_date):
        # Parse input date string
        date_time_obj = datetime.strptime(input_date, '%Y-%m-%d %I:%M:%S %p')

        # Subtract one day
        modified_date = date_time_obj - timedelta(days=1)

        # Format result
        formatted_date = modified_date.strftime('%Y-%m-%d %I:%M:%S %p')

        return formatted_date

    async def minutes_to_time(self,minutes):
        # Calculate hours, minutes, and seconds
        hours = int(minutes / 60)
        remaining_minutes = int(minutes % 60)
        seconds = int((minutes % 1) * 60)

        # Format the result as HH:MM:SS
        formatted_time = '{:02d}:{:02d}:{:02d}'.format(hours, remaining_minutes, seconds)

        return formatted_time

    async def isLateArrival(self,default_work_start_date_time, action_date_time):
        # Parse the datetime strings into datetime objects
        work_start_dt = datetime.strptime(default_work_start_date_time, '%Y-%m-%d %I:%M:%S %p')
        action_dt = datetime.strptime(action_date_time, '%Y-%m-%d %I:%M:%S %p')

        # Compare the datetime objects
        return action_dt > work_start_dt


    async def isEarlyDeparture(self,minutes):
        targetMin = 8 * 60
        calculateMin = minutes - targetMin
        if calculateMin >= 0:
            return False
        else:
            hours, remaining_minutes, seconds =  await self.minutes_to_time(abs(calculateMin))
            return f"{hours} hours, {remaining_minutes} minutes, {seconds} seconds early"

    async def eventMailContent(self,id):


        emailSubject={
            "la":"Late coming notification",
            "ed":"Early departure notification",
            "misL": "Missing lunch break",
            "misD": "Missing departure",
            "d":"Daily Report",
            "m":"Monthly report",

        }

        return emailSubject[id]

    async def lateComingHtml(self, data):

        html_template = """
         <!DOCTYPE html>
         <html lang="en">
         <head>
             <meta charset="UTF-8">
             <meta name="viewport" content="width=device-width, initial-scale=1.0">
             <title>Late coming notification</title>
         </head>
         <body>
             <div style="width:100%; float:left">
                <span style="width:100%; float:left"> Good Morning, {full_name}</span>
                
                <span style="width:100%; float:left; padding:10px, 0px"> Today is : {actionDate}</span>
                <span style="width:100%; float:left;    padding: 7px 7px 7px 0px;"> We have discovered your being late for: <b style="color:red"> {notify_time}</b></span>

                <span style="width:100%; float:left;    padding: 15px 0px 15px 0px;"> 
                Please note that any lateness should be approved by the senior management. Disregard this message if you have informed the senior management about your lateness in advance and got the lateness approved.<br>
                Otherwise, please kindly complete a form of absence indicating the time you have missed. <br>
                Please remember that extra working time later in the day shall not provide sound justification for any voluntary changes of your work schedule except that they have been approved in advance. 
                </span>
                <span style="width:100%; float:left;padding: 5px 0px 25px 0px;"> 
                Strict adherence to the schedule enhances work efficiency and well-being of your colleagues and you. Violation of the schedule jeopardizes the workflow and leads to many undesirable effects such as negative evaluation of your work. 
                </span>


                <span style="width:100%; float:left">
                 Have a nice day! 
                </span> 

                <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                 Regards,
                </span> 

                <span style="width:100%; float:left">
                    Automated Notifications System <br>
                    abcTest Companies Group <br>
                    http://abcTest.com
                </span> 
             <div>
         </body>
         </html>
         """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            notify_time=data['notify_time'],
            actionDate=data['actionDate']
        )
        return formatted_html

    async def earlyDepartureHtml(self, data):

        html_template = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Early departure notification</title>
                </head>
                <body>
                    <div style="width:100%; float:left">
                       <span style="width:100%; float:left"> Hello, {full_name}</span>
                       <span style="width:100%; float:left;    padding: 7px 7px 7px 0px;"> Your working day shortened by: <b style="color:red"> {notify_time}</b></span>

                       <span style="width:100%; float:left;    padding: 15px 0px 15px 0px;"> 

                        Please note that any lateness should be approved by the senior management. <br>
                        Disregard this message if you have informed the senior management about your lateness in advance and got the lateness approved.<br> 
                        Otherwise, please kindly complete a form of absence indicating the time you have missed.  <br>
                        Please remember that extra working time later in the day shall not provide sound justification for any voluntary changes of your work schedule except that they have been approved in advance. 
                       </span>
                       <span style="width:100%; float:left;padding: 5px 0px 25px 0px;"> 
                       Strict adherence to the schedule enhances work efficiency and well-being of your colleagues and you. Violation of the schedule jeopardizes the workflow and leads to many undesirable effects such as negative evaluation of your work. 
                       </span>


                       <span style="width:100%; float:left">
                        Have a nice day! 
                       </span> 

                       <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                        Regards,
                       </span> 

                       <span style="width:100%; float:left">
                           Automated Notifications System <br>
                           abcTest Companies Group <br>
                           http://abcTest.com
                       </span> 
                    <div>
                </body>
                </html>
                """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            notify_time=data['notify_time'],
        )
        return formatted_html



    async def missingLunchHtml(self, data):
        html_template = """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Missing lunch break notification</title>
                        </head>
                        <body>
                            <div style="width:100%; float:left">
                               <span style="width:100%; float:left"> Hello, {full_name}</span>
                               <span style="width:100%; float:left;    padding: 7px 7px 7px 0px;"> We noticed that you missed your scheduled <b style="color:red">lunch break today </b>. </span>

                               <span style="width:100%; float:left;    padding: 15px 0px 15px 0px;"> 

                                Please note that Taking regular breaks is important for maintaining your health and productivity.<br>
                                Please ensure to take your lunch break as scheduled to keep yourself energized and focused.  <br>
                                If you have any questions or need to discuss your schedule, feel free to reach out to your supervisor or the HR department.<br>
                               </span>
                               <span style="width:100%; float:left;padding: 5px 0px 25px 0px;"> 
                               Strict adherence to the schedule enhances work efficiency and well-being of your colleagues and you. Violation of the schedule jeopardizes the workflow and leads to many undesirable effects such as negative evaluation of your work. 
                               </span>


                               <span style="width:100%; float:left">
                                Have a nice day! 
                               </span> 

                               <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                                Regards,
                               </span> 

                               <span style="width:100%; float:left">
                                   Automated Notifications System <br>
                                   abcTest Companies Group <br>
                                   http://abcTest.com
                               </span> 
                            <div>
                        </body>
                        </html>
                        """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            notify_time=data['notify_time'],
        )
        return formatted_html

    async def missingDepartureHtml(self, data):
        html_template = """
                               <!DOCTYPE html>
                               <html lang="en">
                               <head>
                                   <meta charset="UTF-8">
                                   <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                   <title>Missing departure break notification</title>
                               </head>
                               <body>
                                   <div style="width:100%; float:left">
                                      <span style="width:100%; float:left"> Hello, {full_name}</span>
                                      <span style="width:100%; float:left;    padding: 7px 7px 7px 0px;"> We noticed that you missed your scheduled <b style="color:red">Departure time : {notify_time}</b>. </span>

                                      <span style="width:100%; float:left;    padding: 15px 0px 15px 0px;"> 

                                       Please note that Adhering to your scheduled work hours is important for maintaining proper work-life balance and ensuring smooth operation.<br>
                                       Please make sure to follow your departure schedule to avoid any potential issues. <br>
                                       If you have any questions or need to discuss your schedule, feel free to reach out to your supervisor or the HR department.<br>
                                      </span>
                                      <span style="width:100%; float:left;padding: 5px 0px 25px 0px;"> 
                                      Strict adherence to the schedule enhances work efficiency and well-being of your colleagues and you. Violation of the schedule jeopardizes the workflow and leads to many undesirable effects such as negative evaluation of your work. 
                                      </span>
 

                                      <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                                       Regards,
                                      </span> 

                                      <span style="width:100%; float:left">
                                          Automated Notifications System <br>
                                          abcTest Companies Group <br>
                                          http://abcTest.com
                                      </span> 
                                   <div>
                               </body>
                               </html>
                               """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            notify_time=data['notify_time'],
        )
        return formatted_html



    async def dailyReportHtml(self,data):

        work_history_html = ""
        for index, obj in enumerate(data['workHistory']):
            work_history_html += f"""
                  <tr>
                            <td style="width:130px; border: 1px solid #dddddd; padding: 8px; background-color: #f2f2f2;">{index + 1}</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{obj['event_text']}</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{obj['event_action_time']}</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{obj['comments']}</td>
                        </tr>
              """

        html_template = """
                                     <!DOCTYPE html>
                                     <html lang="en">
                                     <head>
                                         <meta charset="UTF-8">
                                         <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                         <title>Daily Report</title>
                                     </head>
                                     <body>
                                         <div style="width:90%; float:left">
                                            <span style="width:100%; float:left"> Hello, {full_name}</span>
                                            <span style="width:100%; float:left;    padding: 7px 7px 7px 0px;"> Below is a summary of  <b style="color:red">{notify_time}</b>. </span>

                                            <span style="width:100%; float:left;    padding: 15px 0px 5px 0px;"> 
                                                  <table style="width: 50%; border-collapse: collapse; margin-bottom: 20px;">
                                                            
                                                            
                                                            <thead>
                                                                   <tr>
                                                                     
                                                                    <th colspan="4" style="text-align:left">Daily report ({notify_time})</th>
                                                               
                                                                   </tr>
                                                                   <tr>
                                                                        <th style="border: 1px solid #dddddd; padding: 2px;background-color: #f2f2f2;">No</th>
                                                                        <th  style="border: 1px solid #dddddd; padding: 2px;background-color: #f2f2f2;">Event NAme</th>
                                                                        <th  style="border: 1px solid #dddddd; padding: 2px;background-color: #f2f2f2;">Time</th> 
                                                                        <th  style="border: 1px solid #dddddd; padding: 2px;background-color: #f2f2f2;">Comments</th> 
                                                                    </tr>
                                                               </thead>
                                                            
                                                            
                                                            <tbody>
                                                              {work_history_html}
                                                            </tbody>
                                                            
                                                            <tfoot>
                                                                   
                                                               <tr>
                                                                   <td colspan="4" style="border: 1px solid #dddddd; padding: 8px;text-align:left">
                                                                   <span style="float:left; margin-right:50px">Total work time : <b>{total_spend_working_time} </b> </span>
                                                                   <span style="float:left; margin-left:10px">Actual work time : <b>{total_actual_working_time} </b> </span>
                                                                   </td>
                                                               </tr>
                                                            </tfoot> 
                                                             
                                                        </table>
 
                                            </span>
                                            <span style="width:100%; float:left;padding: 5px 0px 15px 0px;"> 
                                            If you have any questions or need to discuss your schedule, feel free to reach out to your supervisor or the HR department. 
                                            </span>


                                            <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                                             Regards,
                                            </span> 

                                            <span style="width:100%; float:left">
                                                Automated Notifications System <br>
                                                abcTest Companies Group <br>
                                                http://abcTest.com
                                            </span> 
                                         <div>
                                     </body>
                                     </html>
                                     """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            notify_time=data['notify_time'],
            work_history_html=work_history_html,
            total_spend_working_time=data['total_spend_working_time'],
            total_actual_working_time=data['total_actual_working_time']
        )
        return formatted_html

    async def monthlyReportHtml(self,data):
        work_history_html = ""
        for entry in data['workHistory']:
            aspect, time = list(entry.items())[0]  # Extracting aspect and time
            work_history_html += f"""
                         <tr>
                              
                               <td style="border: 1px solid #dddddd; padding: 8px; background-color: #f2f2f2;">1</td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">Saturday<br>4 May 2024</td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">2:04:24 AM</td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">2:29:19 AM</td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">2 hours</td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">24 mins 55 sec</td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">- 1 hour - 35 mins - 5 sec</td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">dd</td> 
                                <td style="border: 1px solid #dddddd; padding: 8px;"> </td> 
                             
                             
                         </tr>
                     """

        html_template = """
                                            <!DOCTYPE html>
                                            <html lang="en">
                                            <head>
                                                <meta charset="UTF-8">
                                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                                <title>Monthly Report</title>
                                            </head>
                                            <body>
                                                <div style="width:90%; float:left">
                                                   <span style="width:100%; float:left"> Hello, {full_name}</span>
                                                   <span style="width:100%; float:left;    padding: 7px 7px 7px 0px;"> Below is a summary of  <b style="color:red">{notify_time}</b>. </span>

                                                   <span style="width:100%; float:left;    padding: 15px 0px 5px 0px;"> 
                                                         <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                                                                   <thead>
                                                                       <tr>
                                                                           <th colspan="9" style="border: 1px solid #dddddd; padding: 8px;text-align:left">Monthly report ({notify_time})</th>
                                                                       </tr>
                                                                       <tr>
                                                                            <th style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">No</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Date</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Arrival</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Departure</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Lunch break time</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Away time</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Total working time</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Actual working time</th>
                                                                            <th  style="border: 1px solid #dddddd; padding: 8px;background-color: #f2f2f2;">Comments</th> 
                                                                        </tr>
                                                                   </thead>
                                                                   <tbody>
                                                                     {work_history_html}
                                                                   </tbody>
                                                                   <tfoot>
                                                                   
                                                                       <tr>
                                                                           <td colspan="9" style="border: 1px solid #dddddd; padding: 8px;text-align:left">
                                                                           <span style="float:left; margin-right:50px">Total work time : <b>61:33:28 </b> </span>
                                                                           <span style="float:left; margin-left:10px">Actual work time : <b>44:08:15</b> </span>
                                                                           </td>
                                                                       </tr>
                                                                   </tfoot> 
                                                               </table>

                                                   </span>
                                                   <span style="width:100%; float:left;padding: 5px 0px 15px 0px;"> 
                                                   If you have any questions or need to discuss your schedule, feel free to reach out to your supervisor or the HR department. 
                                                   </span>


                                                   <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                                                    Regards,
                                                   </span> 

                                                   <span style="width:100%; float:left">
                                                       Automated Notifications System <br>
                                                       abcTest Companies Group <br>
                                                       http://abcTest.com
                                                   </span> 
                                                <div>
                                            </body>
                                            </html>
                                            """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            notify_time=data['notify_time'],
            work_history_html=work_history_html,
        )
        return formatted_html









    async def eventEmail(self, eventType, email_data):

        to = email_data['to_email']
        subject = email_data['subject']


        # Construct the HTML message
        message=""

        if eventType=="m":
            message = await self.monthlyReportHtml(email_data)

        elif eventType == "d":
            message = await self.dailyReportHtml(email_data)

        elif eventType == "la":
            message = await self.lateComingHtml(email_data)
        elif eventType == "misD":
            message = await self.missingDepartureHtml(email_data)
        elif eventType == "ed":
            message = await self.earlyDepartureHtml(email_data)
        elif eventType == "misL":
            message = await self.missingLunchHtml(email_data)




        mail_config = await self.mail_configuration()
        try:
            with smtplib.SMTP(mail_config['host'], mail_config['port']) as server:
                server.starttls()
                server.login(mail_config['auth']['user'], mail_config['auth']['pass'])

                from_email = f"{mail_config['auth']['name']} <{mail_config['auth']['user']}>"

                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = to
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'html'))

                server.sendmail(mail_config['auth']['user'], to, msg.as_string())
                return True

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Failed to send email: {e}")
            return False






    async def authEmailNotification(self, authEventType, email_data):

        to = email_data['to_email']
        subject = email_data['subject']


        # Construct the HTML message
        message=""

        if authEventType == "userRegi":

            message = await self.userRegistrationHtml(email_data)
        elif authEventType == "changePass":
            message = await self.userPasswordChangeHtml(email_data)



        mail_config = await self.mail_configuration()
        try:
            with smtplib.SMTP(mail_config['host'], mail_config['port']) as server:
                server.starttls()
                server.login(mail_config['auth']['user'], mail_config['auth']['pass'])

                from_email = f"{mail_config['auth']['name']} <{mail_config['auth']['user']}>"

                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = to
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'html'))

                server.sendmail(mail_config['auth']['user'], to, msg.as_string())
                return True

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Failed to send email: {e}")
            return False





    async def authEmailSubject(self,id):


        emailSubject={
            "userRegi":"Registration Confirmation for Time Tracking System (TTS)",
            "changePass":"Your Time Tracking System (TTS) Password Has Been Successfully Changed",
            "sendPass": "Your Time Tracking System (TTS) Password Has Been Successfully Changed",
            "forgetPass":"Your Time Tracking System (TTS) Password Has Been Successfully Changed",
        }

        return emailSubject[id]

    async def userRegistrationHtml(self, data):

        html_template = """
                <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Welcome to Time Tracking System</title>
                        </head>
                        <body>
                            <div style="width:90%; float:left">
                               <span style="width:90%; float:left"> Hello, {full_name}</span>
                               
                               <span style="width:100%; float:left; padding: 7px 7px 7px 0px;">
                               Your registration on Time Tracking System (TTS) has been successfully completed.
                               
                               </span>
                        
                               <span style="width:100%; float:left; padding: 15px 0px 15px 0px;"> 
                                    <p style="color: #555;">Here are some key details about your account.</p>
                                    <p style="color: #555;">Email: {email}</p>
                                    <p style="color: #555;"><b>User-Name:</b> {user_name}</p>
                                    <p style="color: #555;"><b>Password:</b> {password}</p>
                                    
                                    <a target="_blank" href="{website_link}" style="display: inline-block; margin:10px 0px; padding: 10px 20px; font-size: 16px; text-align: center; text-decoration: none; background-color: #4CAF50; color: #fff; border-radius: 5px;"> Go to login</a>
                               </span>
                               
                               <span style="width:100%; float:left;padding: 5px 0px 25px 0px;"> 
                                   Strict adherence to the schedule enhances work efficiency and well-being of your colleagues and you. Violation of the schedule jeopardizes the workflow and leads to many undesirable effects such as negative evaluation of your work. 
                               </span>
                        
                               <span style="width:100%; float:left">
                                Have a nice day! 
                               </span> 
                        
                               <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                                Regards,
                               </span> 
                        
                               <span style="width:100%; float:left">
                                   Automated Notifications System <br>
                                   abcTest Companies Group <br>
                                   http://abcTest.com
                               </span> 
                            </div>
                        </body>
                        </html> 
                """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            email=data['to_email'],
            user_name=data['user_name'],
            password=data['password'],
            website_link=data['website_link'],
        )
        return formatted_html

    async def userPasswordChangeHtml(self, data):

        html_template = """
                <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Successfully changed password</title>
                        </head>
                        <body>
                            <div style="width:90%; float:left">
                               <span style="width:90%; float:left"> Hello, {full_name}</span>

                               <span style="width:100%; float:left; padding: 7px 7px 7px 0px;">
                               Your Time Tracking System (TTS) Password Has Been Successfully Changed

                               </span>

                               <span style="width:100%; float:left; padding: 15px 0px 15px 0px;"> 
                                    <p style="color: #555;">New Login information.</p> 
                                    <p style="color: #555;"><b>User-Name:</b> {user_name}</p>
                                    <p style="color: #555;"><b> New Password:</b> {password}</p>

                                   
                               </span>

                               <span style="width:100%; float:left;padding: 5px 0px 25px 0px;"> 
                                   Strict adherence to the schedule enhances work efficiency and well-being of your colleagues and you. Violation of the schedule jeopardizes the workflow and leads to many undesirable effects such as negative evaluation of your work. 
                               </span>

                               <span style="width:100%; float:left">
                                Have a nice day! 
                               </span> 

                               <span style="width:100%; float:left;padding: 15px 0px 5px 0px;">
                                Regards,
                               </span> 

                               <span style="width:100%; float:left">
                                   Automated Notifications System <br>
                                   abcTest Companies Group <br>
                                   http://abcTest.com
                               </span> 
                            </div>
                        </body>
                        </html> 
                """

        formatted_html = html_template.format(
            full_name=data['full_name'],
            user_name=data['user_name'],
            password=data['password'],
        )
        return formatted_html