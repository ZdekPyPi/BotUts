
@echo off


IF EXIST venv\Scripts\activate (
    venv\Scripts\activate
    IF errorlevel 1 (
        echo ^[7;31merror activating venv[0m
    )
  	
) ELSE (
    echo ^[7;31mvirtual environment not found[0m
)

