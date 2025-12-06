@echo off
set JAVA_HOME=C:\Program Files\Microsoft\jdk-21.0.9.10-hotspot
set PATH=%JAVA_HOME%\bin;%PATH%
uvicorn main:app --reload
