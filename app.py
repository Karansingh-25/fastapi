from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel,Field,computed_field
import pickle 
import pandas as pd
from fastapi.responses import JSONResponse

with open("model.pkl",'rb') as f:
    model=pickle.load(f)

app=FastAPI()

class human(BaseModel):

    Time_spent_Alone:Annotated[int,Field(...,gt=-1,ls=12,description="Time spend alone")]
    Stage_fear:Annotated[bool,Field(...,description="Person have Stage fear?")]
    Social_event_attendance:Annotated[int,Field(...,gt=-1,ls=11,description="Attend social events")]
    Going_outside:Annotated[int,Field(...,gt=-1,ls=7,description="Goes outside?")]
    Drained_after_socializing:Annotated[bool,Field(...,description="Tired after metting with people?")]	
    Friends_circle_size:Annotated[int,Field(...,gt=-1,ls=16,description="Number of friends.")]
    Post_frequency:Annotated[int,Field(...,gt=-1,ls=11,description="Activity on social media")]

    @computed_field
    @property
    def private_time(self)->str:
        if self.Time_spent_Alone < 4:
            return "Low"
        elif self.Time_spent_Alone >=4 and self.Time_spent_Alone < 8:
            return "Medium"
        else :
            return "High"
        
    @computed_field
    @property
    def activity_score(self)->str:
        if self.Social_event_attendance+self.Going_outside+self.Post_frequency <=7:
            return "Low"
        elif self.Social_event_attendance+self.Going_outside+self.Post_frequency >=8 and self.Social_event_attendance+self.Going_outside+self.Post_frequency <=14:
            return "Medium"
        else:
            return "High"
        
    @computed_field
    @property
    def making_friends(self)->str:
        if self.Friends_circle_size < 4:
            return "Low"
        elif self.Friends_circle_size >=4 and self.Friends_circle_size < 9:
            return "Medium"
        else:
            return "High"
        

@app.post('/predict')
def predict(input:human):

    input_df=pd.DataFrame([{
        'private_time':input.private_time,
        'activity_score':input.activity_score,
        'Post_frequency':input.Post_frequency,
        'making_friends':input.making_friends
    }])

    prediction=model.predict(input_df)[0]

    return JSONResponse(status_code=200,content=prediction)