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

QSpinBox::up-arrow, QSpinBox::down-arrow {
    image: url('../icon/icons8-arrow-up-48.png');
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




