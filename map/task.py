# from people.people import People
from collections import deque

from map.action import Action
from people.people import People


class Task:
    STATUS_TODO = 0
    STATUS_DOING = 1
    STATUS_DONE = 2

    def __init__(self):
        self.duration = 0
        self.solution = deque([])
        self.status = Task.STATUS_TODO
        self.need = "general"

    def workingOn(self, workingForce):
        self.duration -= workingForce / 100
        if self.duration <= 0:
            self.status = Task.STATUS_DONE
        else:
            self.status = Task.STATUS_DOING


class MovetoZoneTaskTakeRelease(Task):
    def __init__(self, obj, zone, need, status):
        super().__init__()
        self.need = need
        print(f"moving to {zone}")
        self.solution = deque(
            [
                {"type": Action.TYPE_GOTO_X_Y, "x": obj.x, "velocity": 1.1, "y": obj.y},
                {"type": Action.TYPE_LIFT_OBJ, "obj": obj},
                {
                    "type": Action.TYPE_TASKWORK,
                    "value": 200,
                },
                {"type": Action.TYPE_TAKE_OBJ, "obj": obj},
                {
                    "type": Action.TYPE_GOTO_ZONE,
                    "zone": zone,
                    "velocity": 1.1,
                    "mode": "nearest",
                    "drop": True,
                },
                {"type": Action.TYPE_RELEASE_OBJ},
                {"type": Action.TYPE_PUTDOWN_OBJ, "obj": obj},
                {"type": Action.TYPE_SET_STATUS, "obj": obj, "status": status},
            ]
        )


class CleanObjectRecoverZone(Task):
    def __init__(self, obj, zone):
        super().__init__()
        self.need = "cleaning"
        self.solution = deque(
            [
                {"type": Action.TYPE_GOTO_X_Y, "x": obj.x, "y": obj.y},
                {"type": Action.TYPE_LIFT_OBJ, "obj": obj},
                {
                    "type": Action.TYPE_TASKWORK,
                    "value": 100,
                },
                {"type": Action.TYPE_PUTDOWN_OBJ, "obj": obj},
                {"type": Action.TYPE_MAKE_VISIBLE, "obj": obj, "visible": False},
                {"type": Action.TYPE_RESTORE, "zone": zone, "x": obj.x, "y": obj.y},
            ]
        )


class LeavingGameTask(Task):
    def __init__(self, zone):
        super().__init__()
        self.solution = deque(
            [
                {
                    "type": Action.TYPE_GOTO_ZONE,
                    "zone": zone,
                    "canInterrup": False,
                    "drop": False,
                    "velocity": 0.5,
                },
                {"type": Action.TYPE_PEOPLE_STATUS, "status": People.STATUS_LEAVING},
            ]
        )


class WanderTask(Task):
    def __init__(self, zone):
        super().__init__()
        self.solution = deque(
            [
                {
                    "type": Action.TYPE_GOTO_ZONE,
                    "zone": zone,
                    "canInterrup": True,
                    "drop": False,
                    "velocity": 0.3,
                }
            ]
        )


class MovetoObjWorkOffset(Task):
    def __init__(self, obj, need, value, offset):
        super().__init__()
        self.need = need
        self.solution = deque(
            [
                {
                    "type": Action.TYPE_GOTO_X_Y,
                    "x": obj.x + offset[0],
                    "velocity": 1.1,
                    "y": obj.y + offset[1],
                },
                {"type": Action.TYPE_TASKWORK, "value": value},
                {"type": Action.TYPE_RESTORE_TASK, "obj": obj},
            ]
        )


class MoveConsumeObjMoney(Task):
    def __init__(self, obj, need, value):
        super().__init__()
        self.need = need
        self.obj = obj
        self.solution = deque(
            [
                {
                    "type": Action.TYPE_GOTO_X_Y,
                    "x": obj.x + 1,
                    "velocity": 1.1,
                    "y": obj.y,
                },
                {"type": Action.TYPE_TAKE_OBJ, "obj": obj},
                {
                    "type": Action.TYPE_TASKWORK_OBJ,
                    "need": need,
                    "obj": obj,
                    "value": value,
                    "addGarba": 5,
                },
                {"type": Action.TYPE_RELEASE_OBJ},
                {"type": Action.TYPE_TURN_INTO_GARBAGE, "obj": obj},
            ]
        )


class MoveWorkObjMoney(Task):
    def __init__(self, obj, need, value):
        super().__init__()
        self.need = need
        self.obj = obj
        self.solution = deque(
            [
                {"type": Action.TYPE_GOTO_X_Y, "x": obj.x, "velocity": 1.1, "y": obj.y},
                {
                    "type": Action.TYPE_TASKWORK_OBJ,
                    "need": need,
                    "obj": obj,
                    "value": value,
                    "addGarba": 5,
                },
                {"type": Action.TYPE_RESTORE_TASK, "obj": obj},
            ]
        )


class PrepareDrink(Task):
    ### Go to machine
    ### Work on Machine  (cost?)
    ### Create obj Drink (sin task)
    ###

    def __init__(self, machine, need, value, delivery, serveOn):
        super().__init__()
        self.need = need
        self.type = type
        self.machine = machine
        self.obj = None
        self.serveOn = serveOn
        self.delivery = delivery
        self.solution = deque(
            [
                {"type": Action.TYPE_LOCKED_MACHINE, "machine": self.machine},
                {"type": Action.TYPE_GOTO_OBJ, "obj": self.machine, "velocity": 1.1},
                {
                    "type": Action.TYPE_TASKWORK_OBJ,  ### Work on Machine  (cost?)
                    "need": need,
                    "obj": self.machine,
                    "value": value,
                    "addGarba": 5,
                },
                {
                    "type": Action.TYPE_CREATE_MACHINE_OBJ_ASSIGN,
                    "machine": machine,
                    "delivery": self.delivery,
                    "serveOn": self.serveOn,
                },
                # { "type":Action.TYPE_TAKE_OBJ,
                #   "obj" :self.obj},
                # { "type":Action.TYPE_GOTO_ZONE,
                #   "zone" :DeliveryZone,
                #   "velocity" :1.1,
                #   "mode" : "nearest",
                #   "drop" : True},
                # { "type":Action.TYPE_RELEASE_OBJ},
                # { "type":Action.TYPE_PUTDOWN_OBJ,
                #   "obj" :self.obj},
                # { "type":Action.TYPE_SET_STATUS,
                #   "obj" :self.obj,
                #   "status":status},
            ]
        )
