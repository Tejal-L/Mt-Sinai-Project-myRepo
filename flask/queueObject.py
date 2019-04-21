class QueueObject:
  def __init__(myQueueObject, senderID, payload, queryType, botId):
    myQueueObject.senderID = senderID
    myQueueObject.payload = payload
    myQueueObject.queryType = queryType
    myQueueObject.botId = botId
    

  def printObject(obj):
    print("Current object is " + obj.payload)

#p1 = Person("John", 36)
#p1.myfunc()

