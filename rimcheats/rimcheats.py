from pathlib import Path
import xml.etree.ElementTree as ET
import argparse

SAVE_DIR = Path('/home/dan/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves')

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--alltech", help="Unlock the entire tech tree", action="store_true")
PARSER.add_argument("--mods", help="Print list of active mods", action="store_true")
PARSER.add_argument("--research", help="Print current research progress", action="store_true")
PARSER.add_argument("--upgrade", help="Set all items to \'Excellent\' quality", action="store_true")
# PARSER.add_argument("--game", type=string, help="Optional input save file name", action="store_true")
#
# if args.game:
#     print("Using file: {}".format(args.game()))
#     SAVE = SAVE_DIR / args.game()
# else:
#     print("Using default file: \'project.rws\'")
#     SAVE = SAVE_DIR / 'project.rws'
SAVE = SAVE_DIR / 'project.rws'
TREE = ET.parse(SAVE)
ROOT = TREE.getroot()

def listMods():
    #return list of active mods
    mods = ROOT[0][2]
    modlist = []
    for i in mods:
        modlist.append(i.text)
    return modlist

def listThings():
    #return list of all things (e.g. entities, items, buildings, furniture)
    things = ROOT.findall(".//thing")
    thingList = []
    for thing in things:
        type = thing.find('def').text
        thingList.append(type)
    return thingList

def listPawns():
    #return list of all Pawns (note, this includes entities outside Player faction)
    things = ROOT.findall('.//thing[@Class="Pawn"]')
    thingList = []
    for thing in things:
        type = thing.find('def').text
        thingList.append(type)
    return thingList

def listPlanLocations():
    plans = ROOT.findall('.//designationManager/allDesignations/li[def="Plan"]')
    plansList = []
    for plan in plans:
        planLoc = plan.find('target').text
        plansList.append(planLoc)
    return plansList

def upgradeItems():
    #Checks for all tags with name, "quality" and changes the quality to "Excellent"
    #This will downgrade masterwork items to excellent
    for quality in ROOT.iter('quality'):
        new_quality = 'Excellent'
        quality.text = new_quality
    TREE.write(SAVE)

def researchProgress():
    #Return dictionary of tech tree projects (keys), and progress (values) on each
    research = ROOT.find('.//researchManager/progress')
    keys, values = research.findall('./keys/li'), research.findall('./values/li')
    d = dict()
    for k, v in zip(keys, values):
        d[k.text] = float(v.text)
    return d

def allTech():
    #Instantly unlock the tech tree
    research_progress = ROOT.find('.//researchManager/progress/values')
    for technology in research_progress.iter('li'):
        technology.text = '9999'
    TREE.write(SAVE)

def printList(my_list):
    for item in my_list:
        print(item)

def printDict(my_dict):
    for item in my_dict:
        print("{} - {}".format(item, my_dict[item]))

#print(listMods())
args = PARSER.parse_args()

if args.mods:
    print("listing mods" + "\n")
    printList(listMods())
if args.research:
    print("Research Progress:"+ "\n")
    printDict(researchProgress())
if args.alltech:
    print("Unlocking all tech...")
    allTech()
if args.upgrade:
    print("Upgrading Items...")
    upgradeItems()
