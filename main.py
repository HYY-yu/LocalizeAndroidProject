import json
import re
import sys

import os

regex = "[compile|implementation|androidTestCompile|testImplementation]+ [\'|\"]com.android.support:.+"
defModel = 'model.json'


def loadRootBuildGradle():
    global lines, i, line
    with open(path + 'build.gradle') as rootBGFile:
        lines = rootBGFile.readlines()
    with open(path + 'build.gradle', 'w') as r_w:
        for i, line in enumerate(lines):
            if line.find('repositories') != -1 and not modelDict['mavenRepo'].find('~') != -1:
                new_line = 'maven {url :\'' + modelDict['mavenRepo'] + '\'}\n'
                lines.insert(i + 1, new_line)
            if line.find('classpath \'com.android.tools.build:') != -1 \
                    and not modelDict['gradleTool'].find('~') != -1:
                line = 'classpath \'com.android.tools.build:gradle:' + modelDict['gradleTool'] + '\'\n'
                lines[i] = line
        r_w.writelines(lines)


def loadGradleWrapper():
    global lines, i, line
    with open(path + '/gradle/wrapper/gradle-wrapper.properties') as gwFile:
        lines = gwFile.readlines()
    with open(path + '/gradle/wrapper/gradle-wrapper.properties', 'w') as gwFile_w:
        for i, line in enumerate(lines):
            if line.find('distributionUrl') != -1 and not modelDict['distributionUrl'].find('~') != -1:
                lines[i] = 'distributionUrl=' + modelDict['distributionUrl']
        gwFile_w.writelines(lines)


def loadAllBG():
    global lines, i, line
    for dirA in os.listdir(path):
        if not os.path.isfile(path + dirA) and not dirA.startswith('.'):
            if os.path.isfile(path + dirA + os.sep + 'build.gradle'):
                # load
                dirAFilePath = path + dirA + os.sep + 'build.gradle'
                with open(dirAFilePath) as oneBG_r:
                    lines = oneBG_r.readlines()
                with open(dirAFilePath, 'w') as oneBG_w:
                    for i, line in enumerate(lines):
                        if line.find('compileSdkVersion') != -1 and not modelDict['compileSdkVersion'].find(
                                '~') != -1:
                            lines[i] = '    compileSdkVersion ' + modelDict['compileSdkVersion'] + '\n'
                        if line.find('buildToolsVersion') != -1 and not modelDict['buildToolsVersion'].find(
                                '~') != -1:
                            lines[i] = '    buildToolsVersion \'' + modelDict['buildToolsVersion'] + '\'\n'
                        if line.find('targetSdkVersion') != -1 and not modelDict['targetSdkVersion'].find(
                                '~') != -1:
                            lines[i] = '        targetSdkVersion ' + modelDict['targetSdkVersion'] + '\n'
                        if not modelDict['supportVersion'].find('~') != -1:
                            matchStr = re.search(regex, line)
                            if matchStr:
                                strTemp = matchStr.group()
                                # 跳过multidex
                                if not strTemp.find('multidex') != -1:
                                    a = strTemp.rfind(':') + 1
                                    b = strTemp.rfind('\'')
                                    lines[i] = line.replace(strTemp[a:b], modelDict['supportVersion'])

                    oneBG_w.writelines(lines)


if __name__ == '__main__':
    try:
        path = sys.argv[1]

        if not os.path.exists(path):
            print("path is not exist")
            sys.exit()
        if not os.listdir(path):
            print("empty directory")
            sys.exit()

        if len(sys.argv) > 2:
            if '-j' == sys.argv[2]:
                defModel = sys.argv[3]

        with open(defModel) as f:
            modelDict = json.load(f)

            if not path.endswith(os.sep):
                path += os.sep

            # load #root/build.gradle
            loadRootBuildGradle()

            # load #root/gradle/wrapper/gradle-wrapper.properties
            loadGradleWrapper()

            # load #root/#all_dic_has_build.gradle
            loadAllBG()
    except IndexError:
        print("Please add Android project directory")
        sys.exit(-1)
    except FileNotFoundError:
        print("is it a Android project ?")
        sys.exit(-1)
