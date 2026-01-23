from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from typing import Optional,List


from app.core.database import get_db