from fastapi import FastAPI, Form, HTTPException
from threading import Thread
from fastapi.responses import JSONResponse
from shared.schema import noukriResumeUpdateRequest
from datetime import datetime, timedelta
from app.naukri import naukriAutomation
import logging
from shared.logger import setup_logging
setup_logging()
logger = logging.getLogger('NAUKRILOGGER')

app = FastAPI()

@app.post("/v1/Automation")
async def Automation(request_body: noukriResumeUpdateRequest, status_code=200):
    try:

        login_email = request_body.login_email
        login_password = request_body.login_password

        Input_paras = {'login_email':login_email,'login_password':login_password}
        Input_variables = [key for key, value in Input_paras.items() if value is None]
        
        if Input_variables:
            raise HTTPException(status_code=400, detail=f"Missed parameters : {', '.join(Input_variables)}")
        
        naukri = naukriAutomation()
        update_status = await naukri.updateResume(userName=login_email, password=login_password)
        if update_status:
            return {"status": "SUCCESS","message": f"{login_email} Successfully updated.","statusCode": 200} 
        else:
            return {"status": "FAILED","message": "Failed to update resume.","statusCode": 500}
    except HTTPException as http_exception:
          return JSONResponse(content={"status": "FAILED","detail": http_exception.detail,"status_code":http_exception.status_code}, status_code=http_exception.status_code)
    except  Exception as e:
        return  {"error": str(e)}

