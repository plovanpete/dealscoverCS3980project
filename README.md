# Dealscover
![ApplicationScreenshot](https://github.com/plovanpete/dealscoverCS3980project/assets/145849883/f691d7eb-98e3-46fd-b674-473536716a04)

A work in progress application where you find deals/coupons near you and post them!
(As of now, you can type in coupons or deals and it will only appear at a list. Planning to implement a Map API so that users can click on them and post coupons/deals.)

## Instructions to start it and load it:
For now, you'll need 3 modules: fastapi, uvicorn, and pydantic.
```
python install fastapi uvicorn pydantic
```
You can then run it with this command once those three modules are installed:
```
uvicorn main:app --reload
```

## Descriptions of each file:
**main.py**: The file that allows the server to run.

**coupon.py**: The file that allows the CRUD operations to run in the backend.

**model.py**: The classes that are made for coupon.py

#### _Inside the Frontend Folder_:

**index.html**: The HTML file that is rendered onto the page, uses Bootstrap for styling the buttons,text, and list.

**script.js**: The javascript file that handles the logic and displays messages if things are not filled. Page is automatically updated each time a deal/coupon is created,updated, or deleted.

## Roadmap:
The document and Outline can be found here for final project:
https://docs.google.com/document/d/1uGfQXSzGdjfWUUzGYpOBJLe7kYVDbonJf0ftApabEuU/edit?usp=sharing
