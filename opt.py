from skpy import *

contacts = []
sk = Skype('vijay.kumar@loginworks.com','Vijaykumar')
source_contacts = sk.contacts
#for contact in source_contacts:
contacts.append(str('shekhar.bhardwaj86'))
contacts.append(str('live:vijayks2020'))
contacts.append(str('live:84a5081ce635eb71'))

#contacts.append(str('live:vijay.kumar_105'))
   # print(contacts)
# recent = sk.chats.recent()
#         self.assertEqual(len(recent), 2)
#         # Check the 1-to-1 chat is present.
#         chat = recent["8:{0}".format(Data.contactId)]
#         self.assertEqual(chat.userId, Data.contactId)
#         self.assertEqual(chat.userIds, [Data.contactId])
#         # Check the group chat is present.
#         groupChat = recent[Data.chatThreadId]
#         self.assertEqual(groupChat.creatorId, Data.nonContactId)
#         self.assertEqual(groupChat.adminIds, [Data.nonContactId])
#         self.assertTrue(Data.userId in groupChat.userIds)
#         self.assertTrue(Data.contactId in groupChat.userIds)
#         self.assertTrue(Data.nonContactId in groupChat.userIds)
#         self.assertEqual(groupChat.topic, "Team chat")
#         self.assertTrue(groupChat.open)
#         self.assertTrue(groupChat.history)
for contact in contacts:
    try:
        chat = sk.contacts[contact].chat

        print(sk.chats.recent())
        if chat:
            #print(chat.getMsgs(), '\n')
            if(chat.getMsgs() !=""):
             #print(chat.getMsgs(), '\n')
             for mes in chat.getMsgs():
                 mes.content
              # print(mes.content)
    except Exception as exc:
            resp = exc.args[1]
            #print(resp)