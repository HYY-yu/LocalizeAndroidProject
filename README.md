## LocalizeAndroidProject
打开各种Android工程的小工具 , 快速地将Android工程目录下的gradle插件版本、AndroidSDK版本、Support库版本等等替换。
详细说明见博客：[用脚本秒开一个Android项目](http://blog.csdn.net/csdnyf/article/details/77898606)


# How to use
1. clone this project
2. edit the model.json
3. run : python main.py {path}
> path is a Android Project directory like **/home/feng/AndroidProject/TestProject**

## tip 

- model.json 中你不想修改的属性 ，可以用"~"划掉， 如 ： "targetSdkVersion": "~"
- 大家有什么问题/建议统统砸过来吧～
