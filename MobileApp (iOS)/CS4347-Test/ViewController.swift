//
//  ViewController.swift
//  CS4347-Test
//
//  Created by Russell Ong on 13/3/21.
//

import UIKit
import AVFoundation


class ViewController: UIViewController {
    let failedText = "Failed to Play Music"
    let successText = "Playing Music!"
    let library = ["Babooshka", "A Thousand Years", "A Good Heart", "A Kind of Magic", "A Little Respect"]
    var player: AVMIDIPlayer = AVMIDIPlayer()
    let req = RequestHandler()
    var file = ""
    var selectedMIDI = ""
    var isSelected = false
    var selectedSoundBank = "soundbank1"
    
    let picker = UIPickerView()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        picker.delegate = self
        setupUI()
    }
    
    @IBOutlet weak var midiLabel: UILabel!
    @IBOutlet weak var statusLabel: UILabel!
    
    fileprivate func setupUI(){
        self.view.backgroundColor = UIColor(patternImage: UIImage(named: "bg")!)
        picker.alpha = 0
        picker.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(picker)

        picker.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor).isActive = true
        picker.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor).isActive = true
        picker.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor).isActive = true
    }
    
    fileprivate func playMusic(url: String){
        let documentsDirectoryURL =  FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        let destinationURL = documentsDirectoryURL.appendingPathComponent(url)

        guard let soundBankUrl = Bundle.main.path(forResource: selectedSoundBank, ofType: "sf2") else { return print("error loading soundbank")
        }
        let soundbankfile = URL(string: soundBankUrl)

        do {
            try player = AVMIDIPlayer(contentsOf: destinationURL, soundBankURL: soundbankfile)
            player.prepareToPlay()
            statusLabel.text = successText
            player.play {
                print("finished playing")
            }
        } catch {
            print("could not create MIDI player")
            statusLabel.text = failedText
        }
    }
    
    @IBAction func selectBtnTapped(_ sender: Any) {
        if isSelected {
            picker.alpha = 0
        } else {
            picker.alpha = 1
        }
        isSelected = !isSelected
        
        statusLabel.text = "File Selected"
    }
    
    @IBAction func postBtnTapped(_ sender: Any) {
        statusLabel.text = "Sending MIDI file..."
        req.postMIDI(file: selectedMIDI) { status in
            self.statusLabel.text = status
        }
    }
    
    @IBAction func getBtnTapped(_ sender: Any) {
        req.getMIDI { newFile in
            self.file = newFile
            self.statusLabel.text = "File Downloaded"
        }
    }
    
    @IBAction func playBtnTapped(_ sender: Any) {
        playMusic(url: file)
    }
    
    @IBAction func stopBtnTapped(_ sender: Any) {
        player.stop()
        statusLabel.text = "Stopping Music..."
    }
    
    @IBAction func synthBtnTapped(_ sender: Any) {
        selectedSoundBank = "soundbank1"
        statusLabel.text = "Synth Soundbank Selected"
    }
    
    @IBAction func amongUsBtnTapped(_ sender: Any) {
        selectedSoundBank = "soundbank2"
        statusLabel.text = "AmongUs Soundbank Selected"
    }
    
    @IBAction func pianoBtnTapped(_ sender: Any) {
        selectedSoundBank = "soundbank3"
        statusLabel.text = "Piano Soundbank Selected"
    }
}

extension ViewController: UIPickerViewDataSource, UIPickerViewDelegate {
    public func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    public func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return library.count
    }
    
    public func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return library[row]
    }
    
    public func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        selectedMIDI = library[row]
        midiLabel.text = selectedMIDI
    }
    
}
