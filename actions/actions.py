# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from bs4 import BeautifulSoup
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionStateData(Action):

    def name(self) -> Text:
        return "action_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities=tracker.latest_message['entities']
        print(entities)
        
        
        r=requests.get('https://api.rootnet.in/covid19-in/stats/history')

        r.reason
        x=r.json()


        y=dict(x)
        all_states_data=y['data'][-1]['regional']
        states_index={}
        j=0
        for i in all_states_data:
            states_index[i['loc']]=j
            j=j+1

        opr=''
        state_name=[]
        ans=0
        print(len(entities))
        for e in entities:
            if e['entity']=='State':
                state_name.append(e['value'])
            if e['entity']=='opr':
                opr=e['value']
                
            # message=str(all_states_data[states_index[name]]['confirmedCasesIndian'])
        if opr == 'altogether':
            for i in state_name:
                ans=ans+all_states_data[states_index[i]]['totalConfirmed']
        else:
            ans=all_states_data[states_index[state_name[0]]]['totalConfirmed']
        print(ans)
        dispatcher.utter_message(text=str(ans))

        return []


class ActionDateData(Action):

    def name(self) -> Text:
        return "action_date_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities=tracker.latest_message['entities']
        print(entities)
        
        
        r=requests.get('https://api.rootnet.in/covid19-in/stats/history')

        r.reason
        x=r.json()


        y=dict(x)
        all_days=y['data']
        day_index={}
        j=0
        for i in all_days:
            day_index[i['day']]=j
            j=j+1
        date=[]
        day=[]
        month=[]
        year=[]
        ans=0
        opr=''
        for e in entities:
            if e['entity']=='day':
                day.append(e['value'])
            if e['entity']=='month':
                month.append(e['value'])
            if e['entity']=='year':
                year.append(e['value'])
            
            try:
                if e['entity']=='operation':
                    opr=e['value']
            except AttributeError:
                opr=''
        try:
            date.append(year[0]+"-"+ month[0]+"-"+ day[0])
        except IndexError:
            date
        try:
            date.append(year[1]+"-"+ month[1]+"-"+ day[1])
        except IndexError:
            date
        if opr=='to':
            for i in range(day_index[date[0]],day_index[date[1]]+1):
                ans=ans+all_days[i]['summary']['total']
        else:
            ans=all_days[day_index[date[0]]]['summary']['total']

        # message=str(all_states_data[states_index[name]]['confirmedCasesIndian'])

        dispatcher.utter_message(text=str(ans))

        return []
