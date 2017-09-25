import pymongo
client = pymongo.MongoClient('localhost', 8089)
cm = client['console']
cm.authenticate('waqu_cm', 'cm@123457')
print('ok')

f = open('toyvideo_wid_tag_r', 'w')

with open("wid") as fh:
    for line in fh:
        wid = line.strip('\n')
        vv=cm.videos.find_one({'wid':wid},{"wid":1,"toyTags":1})
        list=vv.get('toyTags')
        str=''
        if list==None or len(list)==0:
            continue
        for s in list:
            f.write('%s\t%s\r\n' % (vv.get("wid"), s))




f.close()
client.close()