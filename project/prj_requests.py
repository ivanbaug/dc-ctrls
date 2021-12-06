import os
from typing import Tuple
import requests
import json
from requests.exceptions import HTTPError
from dotenv import load_dotenv


load_dotenv(".env")
API_SELECT_URL = os.environ.get("API_SELECT_URL")

with open("project\\test.json", "r") as f:
    devices_data = json.load(f)


def select_from_all(di: int = 0, ai: int = 0, do: int = 0, ao: int = 0):
    try:
        response = requests.post(
            f"{API_SELECT_URL}/dcCtrlSelect",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"di": di, "ai": ai, "do": do, "ao": ao}),
        )
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
        req = [di, ai, do, ao]
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
    except Exception as err:
        print(f"Other error occurred: {err}")  # Python 3.6
    else:
        selected = response.json()["results"]
        # for s in selected:
        #     print(s["name"])
        return list_possible_ctrls(req, selected, devices_data)


def prove_io(required: int, base: int, universal: int) -> Tuple:
    """Returns free io after using 'base' and 'universal' io to fullfill the 'required' io.
    Parameters:
        required (int): required io (analog / digital)
        base (int): available io, single use (analog or digital)
        universal (int): universal io available (can cover analog and digital use case)
    """
    if required > 0:
        required = required - base
        if required > 0:
            base = 0
            required = required - universal
            if required > 0:
                universal = 0
            else:
                universal = abs(required)
                required = 0
        else:
            base = abs(required)
            required = 0
    return (required, base, universal)


# TODO: Implement the following to display the devices


def prove_device(req: list, device: list) -> Tuple:
    """Returns used io, missing required io and remaining io after fullfilling requirement."""
    # Requirement
    rDI = req[0]
    rAI = req[1]
    rDO = req[2]
    rAO = req[3]

    # Available
    dDI = device[0]
    dAI = device[1]
    dUI = device[2]
    dDO = device[3]
    dAO = device[4]
    dUO = device[5]

    # f stands for free outputs, inputs, and universal
    rAI, fAI, fUI = prove_io(rAI, dAI, dUI)
    rDI, fDI, fUI = prove_io(rDI, dDI, fUI)
    rAO, fAO, fUO = prove_io(rAO, dAO, dUO)
    rDO, fDO, fUO = prove_io(rDO, dDO, fUO)

    req = [rDI, rAI, rDO, rAO]
    remainders = [fDI, fAI, fUI, fDO, fAO, fUO]
    used = [dDI - fDI, dAI - fAI, dUI - fUI, dDO - fDO, dAO - fAO, dUO - fUO]

    return (used, req, remainders)


def create_module_dict(name, used_io):
    m_dict = {}
    m_dict["name"] = name
    m_dict["di"] = used_io[0]
    m_dict["ai"] = used_io[1]
    m_dict["ui"] = used_io[2]
    m_dict["do"] = used_io[3]
    m_dict["ao"] = used_io[4]
    m_dict["co"] = used_io[5]
    return m_dict


def list_possible_ctrls(req, ctrl_sol_list, ddata):
    # req : requirements
    # ctrl_sol_list : list of controller selections
    # ctrls : general list of available controller objects
    # exs : general list of available expansion module objects
    main_list = []
    ctrls = ddata["ctrls"]
    exs = ddata["exps"]

    print("listing possible ctrls")
    for c in ctrl_sol_list:
        dev_list = []
        devices = c["name"].split()

        # Find the controller data
        controller = next(item for item in ctrls if item["name"] == devices[0])
        used_io, new_required, _ = prove_device(
            req=req,
            device=[
                controller["di"],
                controller["ai"],
                controller["ui"],
                controller["do"],
                controller["ao"],
                controller["co"],
            ],
        )
        dev_list.append(create_module_dict(devices[0], used_io=used_io))

        # Iterate over expansion modules to add exps data
        for ex in devices[1:]:
            expansion = next(item for item in exs if item["name"] == ex)
            used_io, new_required, _ = prove_device(
                req=new_required,
                device=[
                    expansion["di"],
                    expansion["ai"],
                    expansion["ui"],
                    expansion["do"],
                    expansion["ao"],
                    expansion["co"],
                ],
            )
            dev_list.append(create_module_dict(ex, used_io=used_io))

        # Get total available io's
        _, _, total_remaining = prove_device(
            req,
            [
                c["di"],
                c["ai"],
                c["ui"],
                c["do"],
                c["ao"],
                c["co"],
            ],
        )
        dev_list.append(create_module_dict("Available", total_remaining))

        option_dict = {"device_summary": dev_list, "cost": c["cost"]}
        main_list.append(option_dict)

    return main_list


# print(devices_data['ctrls'][0])
# print(select_from_all(6, 2, 3, 3))
