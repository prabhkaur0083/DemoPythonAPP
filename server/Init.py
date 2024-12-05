from fastapi import FastAPI
from routes.user.SignUp import SignUpRouter
from routes.user.Login import LoginRouter
from routes.user.DeleteToken import DeleteTokenRouter
from routes.user.VerifyToken import TokenVerifyRouter
from routes.report.ExtractVisuals import VisualRouter
from routes.report.ExtractJsonData import VisualJsonRouter
from routes.report.FIlterData import DataFilterRouter

app = FastAPI()

# Base Router For All Endpoints
app.include_router(SignUpRouter, prefix="/api/v1/user")
app.include_router(LoginRouter, prefix="/api/v1/user")
app.include_router(DeleteTokenRouter, prefix="/api/v1/usertoken")
app.include_router(TokenVerifyRouter, prefix="/api/v1/usertoken")
app.include_router(VisualRouter, prefix="/api/v1/report/visual")
app.include_router(VisualJsonRouter, prefix="/api/v1/report/visualJson")

# Drill through 
app.include_router(DataFilterRouter,prefix="/api/v1/report/filterData")