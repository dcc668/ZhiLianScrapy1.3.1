#!  /usr/bin/env python
#ecoding=utf-8
import chardet
class EncodingUtils:
    #byteTarget 字节类型数据
    @staticmethod
    def getStrNotKnowEcoding(byteTarget):
        json = chardet.detect(byteTarget);
        htmlStr = EncodingUtils.decodeAndEncode(byteTarget, json["encoding"]);
        return htmlStr;

    @staticmethod
    def decodeAndEncode(target,decode):
        if 'utf-8'==decode:
            htmlStr = str(target, "utf-8")  # toString
        else:
            bhtml = target.decode(decode).encode("utf-8")
            htmlStr = str(bhtml, "utf-8")  # toString
        return htmlStr