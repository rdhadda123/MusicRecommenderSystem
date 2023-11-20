'''
Created on 11/9/23
Authors: Rishabh Dhadda, Chloe Tu, Jonathan Kwon
Pledge: I pledge my Honor that I have abided by the Stevens Honor System.
'''
PREF_FILE = 'musicrecplus.txt'

from os import path

def menu(name, preferences, userMap, fileName):
    """Prints out menu interface for user and allows user to navigate through interface. (Rishabh and Chloe)""" 
    while True:
        print("Enter a letter to choose an option:")
        print("e - Enter preferences")
        print("s - Get current preferences")
        print("r - Get recommendations")
        print("p - Show most popular artists")
        print("h - How popular is the most popular")
        print("m - Which user has the most likes")
        print("q - Save and quit")

        selection = input()

        if selection == "e":
            newPreferences(name, userMap)
        elif selection == "s":
            showPreferences(name, userMap)
        elif selection == "r":
            recommendations = getRecommendations(preferences, name, userMap)
            if not recommendations:
                print('No recommendations available at this time.')
            else:
                for artist in recommendations:
                    print(artist)
        elif selection == "p":
            popularArtists(name, preferences, userMap)
        elif selection == "h":
            howPopular(preferences, name, userMap)
        elif selection == "m":
            mostLikes(userMap)
        elif selection == "q":
            saveNquit(name, preferences, userMap, fileName)
        else:
            print("Invalid value")

def newPreferences(userName, userMap):
    '''creates a new list for the artists the user likes (Rishabh)'''
    l = []
    while True:
        print('Enter an artist that you like (Enter to finish):')
        name = input()
        if name == '':
            break
        l.append(name.title())
    if userName in userMap:
        userMap[userName] += l
    else:
        userMap[userName] = l
    return l

def getPreferences(userName, userMap):
    """Returns a list of the user's preferred artists. If the system already knows about the user, 
    it gets the preference out of the userMap dictionary and then asks the user if they have additional preferences. 
    If the user is new, it simply asks the user for their preferences. (Chloe and Jonathan)"""
    if userName in userMap:
        prefs = userMap[userName]
    else:
        prefs = newPreferences(userName,userMap)

    return prefs

def showPreferences(userName, userMap):
    """Displays the user's current music preferences. (Jonathan)"""
    if userName in userMap:
        prefs = userMap[userName]
        print("Your current music preferences include:")
        for artist in prefs:
            print(artist)
    else:
        print("No preferences available for this user.")

def mostLikes(userMap): 
    """Prints out the most liked artist that the user has. If there is no artists with any likes, it prints the message 'Sorry, no user found. (Jonathan)"""
    userArtistQuantityList=[]
    for user in userMap:
        userArtistQuantityList.append((len(userMap[user]),user))
    userArtistQuantityList.sort()
    if len(userArtistQuantityList)==0:
        print('Sorry, no user found.')
    else:
        print(userArtistQuantityList[-1][1])

def popularArtists(name, preferences, userMap): 
    """Prints the most popular artists in the text file. Increases the count while artistsInPublicTextList isn't empty. 
    to your like list once the length of it is 1 or empty. (Jonathan and Rishabh)"""
    
    artistsInPublicTextList=[]
    for user in userMap:
        if user.endswith('$') or user == name:
            continue 
        artistsInPublicTextList += userMap[user]

    artistsInPublicTextList.sort()

    artistLikingList = []
    count = 1

    while artistsInPublicTextList:
        if len(artistsInPublicTextList) == 1:
            artistLikingList.append((count, artistsInPublicTextList[0]))
        elif artistsInPublicTextList[0] == artistsInPublicTextList[1]:
            count += 1
        else:
            artistLikingList.append((count, artistsInPublicTextList[0]))
            count = 1
        artistsInPublicTextList = artistsInPublicTextList[1:]

    artistLikingList.sort()

    if artistLikingList:
        for count, artist in reversed(artistLikingList):
            print(artist)
    else:
        print("\n".join(preferences))

    return artistLikingList

def howPopular(preferences, name, userMap):
    '''Returns how popular the most popular artist is (Rishabh)'''
    artists = {}
    for i in preferences:
        i = i.strip()
        if i in artists:
            artists[i] += 1
        else:
            artists[i] = 1
    for user in userMap:
        if '$' not in user and user.lower().strip() != name.lower().strip():
            liked_artists = userMap[user]
            for i in liked_artists:
                i = i.strip()
                if i in artists:
                    artists[i] += 1
                else:
                    artists[i] = 1
    if len(artists) == 0:
        print('Sorry, no artists found.')
    else:
        print(max(artists.values()))

def loadUsers(fileName):
    """Reads in a file of stored users' preferences stored in the file 'fileName'. 
    Returns a dictionary containing a mapping of user names to a list of preferred artists (Chloe)"""
    if not path.exists(fileName):
        print(f"Error: File '{fileName}' not found.")
        return {}

    userDict = {}
    with open(fileName, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            parts = line.split(':')
            if len(parts) == 2:
                userName, bands = parts
                bandList = bands.split(',')
                bandList.sort()
                userDict[userName] = bandList

    return userDict

def getRecommendations(preferences, name, userMap):
    '''returns recommendations based on similar users, if none it will return 'no recommendations at this time' (Rishabh and Jonathan)'''
    count = 0
    highest = (0, [])
    for user in userMap:
        if '$' not in user and user != name:
            count = 0
            userPreferences = userMap[user]
            for artist in preferences:
                artist = artist.strip()
                if artist in userPreferences:
                    count += 1
                if count > highest[0]:
                    highest = (count, userPreferences)
                if highest[0] == len(preferences):
                    highest = (0, [])
    if len(highest[1]) == 0:
        return []
    else:
        all_present = all(artist.strip() in preferences for artist in highest[1])
        if all_present:
            print('No recommendations available at this time')
        else:
            return [artist.strip() for artist in highest[1] if artist.strip() not in preferences]



def drop(list1, list2):
    """Return a new list that contains only the elements in list2 that were NOT in list1.(Chloe)"""
    list3 = []
    i = 0
    j = 0
    while i<len(list1) and j<len(list2):
        if list1[i] == list2[j]:
            print("Skipping", list1[i])
            i+=1
            j+=1
        elif list1[i]<list2[j]:
            i+= 1
        else:
            list3.append(list2[j])
            j+= 1
    while j < len(list2):
        list3.append(list2[j])
        j+= 1
    return list3

def numMatches(list1, list2):
    """return the number of elements that match between two sorted lists (Chloe)"""
    matches = 0
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list[i] == list2[j]:
            matches += 1
            i+=1
            j+=1
        elif list[i] < list2[j]:
            i+=1
        else:
            j+= 1
    return matches

def saveUserPreferences(userName, prefs, userMap, fileName):
    '''Saves the user preferences in the txt file (Rishabh)'''
    userMap[userName] = prefs
    with open(fileName, 'w') as file:
        for user in sorted(userMap):
            file.write(f"{user}:{','.join(userMap[user])}\n")

def saveNquit(userName, prefs, userMap, fileName):
    '''Saves the preferences and exits the program (Rishabh)'''
    saveUserPreferences(userName, prefs, userMap, fileName)
    exit()


def main():
    userMap = loadUsers(PREF_FILE)

    print('Enter your name (put a $ symbol after your name if you wish your preferences to remain private): ')
    userName = input()

    prefs = getPreferences(userName, userMap)

    while True:
        menu(userName, prefs, userMap, PREF_FILE)

main()
