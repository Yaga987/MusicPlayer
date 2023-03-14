import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QFileDialog, QStyle, QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QUrl, QPropertyAnimation
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

# define the colors as a QColor object
red_color = QColor(255, 25, 25)
orange_color = QColor(255, 135, 25)
black_color = QColor(255, 255, 255)
white_color = QColor(0, 0, 0)

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 600, 400)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.setVolume(50)
        self.setStyleSheet(f"background-color: {white_color.name()}; color: {red_color.name()}; selection-color: {orange_color.name()} ;selection-background-color: {black_color.name()};")

        # create buttons
        self.playBtn = QPushButton("Play")
        self.playBtn.setStyleSheet(f"background-color: {orange_color.name()}; color: {black_color.name()}; selection-color: {red_color.name()} ;selection-background-color: {white_color.name()};")
        # self.playBtn.setStyleSheet("background-color: darkorange; color: black;")
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_music)

        self.pauseBtn = QPushButton("Pause")
        self.pauseBtn.setStyleSheet(f"background-color: {orange_color.name()}; color: {black_color.name()}; selection-color: {red_color.name()} ;selection-background-color: {white_color.name()};")
        # self.pauseBtn.setStyleSheet("background-color: red; color: black;")
        self.pauseBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pauseBtn.clicked.connect(self.pause_music)

        self.stopBtn = QPushButton("Stop")
        self.stopBtn.setStyleSheet(f"background-color: {orange_color.name()}; color: {black_color.name()}; selection-color: {red_color.name()} ;selection-background-color: {white_color.name()};")
        # self.stopBtn.setStyleSheet("background-color: black; color: white;")
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop_music)

        self.quitBtn = QPushButton("Quit")
        self.quitBtn.setStyleSheet(f"background-color: {orange_color.name()}; color: {black_color.name()}; selection-color: {red_color.name()} ;selection-background-color: {white_color.name()};")
        # self.quitBtn.setStyleSheet("background-color: red; color: black;")
        self.quitBtn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        self.quitBtn.clicked.connect(self.close)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setTickPosition(QSlider.TicksBelow)
        self.volumeSlider.setTickInterval(10)
        self.volumeSlider.valueChanged.connect(self.change_volume)

        # create song name label
        self.songLabel = QLabel()
        self.songLabel.setAlignment(Qt.AlignCenter)

        # set up animation to fade in and out the label's background color
        self.labelAnimation = QPropertyAnimation(self.songLabel, b"styleSheet")
        self.labelAnimation.setDuration(1000)
        self.labelAnimation.setLoopCount(-1)
        self.labelAnimation.setStartValue(f"background-color: {orange_color};")
        self.labelAnimation.setEndValue(f"background-color: {red_color};")
        self.labelAnimation.start()
        
        # connect mediaPlayer's metaDataChanged signal to update_song_label
        self.mediaPlayer.metaDataChanged.connect(self.update_song_label)

        # create layout
        gridLayout = QGridLayout()
        gridLayout.addWidget(self.songLabel, 0, 0, 1, 3) # song name label at the top
        gridLayout.addWidget(self.playBtn, 1, 0)
        gridLayout.addWidget(self.pauseBtn, 1, 1)
        gridLayout.addWidget(self.stopBtn, 1, 2)
        gridLayout.addWidget(self.volumeSlider, 2, 0, 1, 3)
        gridLayout.addWidget(self.quitBtn, 3, 2)
        self.setLayout(gridLayout)

    def play_music(self):
        fileUrl, _ = QFileDialog.getOpenFileUrl(self, "Open Audio File", QUrl(os.path.expanduser('~')), "Audio Files (*.mp3 *.wav)")
        if fileUrl:
            self.mediaPlayer.setMedia(QMediaContent(fileUrl))
            self.mediaPlayer.play()

    def pause_music(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playbackPosition = self.mediaPlayer.position()
        else:
            self.mediaPlayer.play()
            self.mediaPlayer.setPosition(self.playbackPosition)

    def update_song_label(self):
        title = self.mediaPlayer.metaData('Title')
        self.labelAnimation.start() # start animation
        if title:
            self.songLabel.setText(title)
        else:
            self.songLabel.setText('Unknown')

        self.labelAnimation.stop() # stop animation
        self.songLabel.setStyleSheet(f"background-color: {orange_color};") # reset label's background color

    def stop_music(self):
        self.mediaPlayer.stop()
        self.songLabel.setText('')

    def change_volume(self):
        self.mediaPlayer.setVolume(self.volumeSlider.value())

    def closeEvent(self, event):
        self.stop_music()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    music_player = MusicPlayer()
    music_player.show()
    sys.exit(app.exec_())