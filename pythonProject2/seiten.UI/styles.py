
style_box = """
QComboBox {
    border: 2px solid #60a698;
    border-radius: 5px;
    padding: 5px;
    background-color: #F0F8FF;
    color: #333;
    font-size: 18px;

}

QComboBox:hover {
    border-color: #0078D7;
}

QComboBox::drop-down {
   border-left: 1px solid #60a698;
    background-color: #D9F1FF;
    width: 30px;
}

QComboBox::down-arrow {
    image: url(../icon/down_arrow_icon.png);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    border: 1px solid #60a698;
    background-color: #FFFFFF;
    selection-background-color: #0078A4;
    selection-color: #FFFFFF;
    padding: 5px;
}
QSpinBox {
    border: 2px solid #60a698;
    border-radius: 5px;
    padding: 5px;
    background-color: #FFFFFF;
    color: #333;
    font-size: 18px;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #D9F1FF;
    border: none;
    width: 16px;
    height: 16px;
}

QSpinBox::up-arrow {
    image: url('../icon/up-arrow.png');
    width: 12px;
    height: 12px;
}
QSpinBox::down-arrow {
    image: url('../icon/down-arrow.png');
    width: 12px;
    height: 12px;

}

"""

city_section_style = """
QLabel#city_title {
    font-size: 20px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}

QScrollArea {
    border: 2px solid #60a698;
    border-radius: 5px;
    background-color: #F0F8FF;
}

QScrollBar:vertical {
    border: none;
    background: #D9F1FF;
    width: 10px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: #60a698;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}

QPushButton {
    border: 0.5px solid #60a698;
    border-radius: 5px;
    background-color: #FFFFFF;
    padding: 0px;
}

QPushButton:checked {
    background-color: #D9F1FF;
    border: 2px solid #0078A4;
}
"""
reset_button_style = """
    QPushButton {
        background-color: #F0F8FF;
        color: #333;
        font-size: 18px;
        padding: 8px 15px;
        border: 2px solid #60a698;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #D9F1FF;
        border-color: #0078D7;
    }
    QPushButton:pressed {
        background-color: #0078A4;
        color: #FFF;
    }
"""

search_button_style = """
    QPushButton {
        background-color: #60a698;
        color: #FFF;
        font-size: 18px;
        padding: 8px 15px;
        border: 2px solid #60a698;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #0078D7;
        border-color: #005C99;
    }
    QPushButton:pressed {
        background-color: #005C99;
        color: #FFF;
    }
"""

footer_prev_style="""
    QPushButton {
        background-color: #B0BEC5; 
        color: white;            
        border: none;             
        border-radius: 8px;      
        font-size: 16px;         
        transition: background-color 0.3s; 
        padding:8px;
        } 
        QPushButton:hover {
            background-color: #90A4AE;
        }  
         QPushButton:pressed {
            background-color: #78909C;
        }
    """

footer_next_style="""
     QPushButton {
         background-color: #4CAF50; 
         color: white;            
         border: none;                  
         border-radius: 8px;               
         transition: background-color 0.3s; 
         padding:8px;
    }

    QPushButton:hover {
        background-color: #45A049; 
    }

    QPushButton:pressed {
        background-color: #388E3C;
        }

    QPushButton:icon {
        color: white;             
        }
    """

menu_style = """
QPushButton {
    background-color: #60a698;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: #0078D7;
}
QPushButton:pressed {
    background-color: #005C99;
}
"""


back_button_style = """
    QPushButton {
        background-color: #60a698;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #e6e6e6;
        border-color: #aaa;
    }
    QPushButton:pressed {
        background-color: #dcdcdc;
        border-color: #888;
    }
    QPushButton:disabled {
        background-color: #f9f9f9;
        color: #aaa;
        border-color: #ddd;
    }
"""

choose_button_style = """
QPushButton {
    font-size: 16px;
    border: 2px solid #007bff;
    border-radius: 8px;
    color: white;
    background-color: #007bff;
}
QPushButton:hover {
    background-color: #00bcff;
 
}
"""

Qlist_style = """
QListWidget{
 font-size: 24px; 
}

"""
city_button_style = """
    QPushButton {
        border: 2px solid black;
        border-radius: 8px;
        background-color: white;
        color: black;
        font-size: 14px;
        padding: 5px;
    }
    QPushButton:hover {
        border: 2px solid #007bff;
        background-color: #e6f2ff;
    }
    QPushButton:checked {
        border: 2px solid blue;
        background-color: lightblue;
        color: white;
    }
"""
loginmainstyle = """
    QMainWindow {background-color: #f0f5f9; }
            QPushButton {
                font-size: 16px;
                background-color: #0078d7;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLineEdit {
                font-size: 16px;
                padding: 12px;
                border: 1px solid #a0a0a0;
                border-radius: 5px;
            }
            QLabel {
                font-size: 18px; 
                color: #333; 
    }
"""
loginlabelstyle = """
    Qlabel {
        font-size: 16px;
        color: #333;
    }
"""

loginbuttonstyle = """
    QPushButton {
        font-size: 18px;
        background-color: #0078d7;
        color: white;
        padding: 12px;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #005a9e;
    }
"""
logintitlestyle = """
    QLabel {
        font-size: 20px;
        font-weight: bold;
        color: #0078d7;
    }
"""
loginimagestyle="""
    QLabel{
        border:none;
        margin: 0 auto;
        
    }

"""
registerpromptstyle="""
    QPushButton {
        color: #0078d7;
        font-size: 16px; 
        cursor: pointer; 
        border: none;
        background-color : transparent;
    }
"""

Datestyle = """
    QDateEdit {
        font-size: 18px;
        padding: 10px;
        border: 2px solid #60a698;
        border-radius: 5px;
    }

"""

cancelstyle = """
QPushButton {
       background-color: red;
       color: white;
       font-size: 16px;
       font-weight: bold;
       padding: 10px 20px;
       border: none;
       border-radius: 8px;
   }
   QPushButton:hover {
       background-color: darkred;
   }
   QPushButton:pressed {
       background-color: crimson;
   }
   """
validbtnstyle = """
QPushButton {
        background-color: #007bff;
        color: white;
        font-size: 16px;
        padding: 8px 16px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #0056b3;
    }

"""
confirmbtnstyle = """
QPushButton {
                background-color: green;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }


"""

confirmbtnstyledisable = """
QPushButton {
                background-color: lightgray;
                color: gray;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }


"""
