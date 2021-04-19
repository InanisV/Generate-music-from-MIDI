//
//  PostMidi.swift
//  CS4347-Test
//
//  Created by Russell Ong on 31/3/21.
//

import Alamofire

class RequestHandler {
    var postUrl = "http://ec2-54-169-251-110.ap-southeast-1.compute.amazonaws.com/generate"
    var getUrl = "http://ec2-54-169-251-110.ap-southeast-1.compute.amazonaws.com/getfile/LakhMIDI_midi_g.mid"
    
//    var loadDownloadUrl = "https://files.khinsider.com/midifiles/gameboy/pokemon-red-blue-yellow-/pokemon-center.mid"
    
//    func loadMIDI(_ completion: @escaping (String) -> ()) {
//        let destination: DownloadRequest.Destination = { _, _ in
//            let documentsURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
//            let fileURL = documentsURL.appendingPathComponent("load.mid")
//
//            return (fileURL, [.removePreviousFile, .createIntermediateDirectories])
//        }
//        AF.download(loadDownloadUrl, to: destination).validate().responseData(completionHandler: { response in
//            guard let fileUrl = response.fileURL else {return print("failed to open file URL")}
//            completion(fileUrl.lastPathComponent)
//        })
//    }
    
    func postMIDI(file: String, _ completion: @escaping (String) -> ()) {
        print("posting...")
        
        //this is for stuff found on local
        guard let localFile = Bundle.main.url(forResource: file, withExtension: "mid") else {
            return completion("LocalFile Error")
        }
        
//        // this is for downLOADED content
//        let documentsDirectoryURL =  FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
//        let fileURL = documentsDirectoryURL.appendingPathComponent(file)
        
        guard let midiFile: Data = try? Data(contentsOf: localFile) else {return completion("error opening MIDI")}
        AF.upload(multipartFormData: { multipartFormData in
            multipartFormData.append(midiFile, withName: "midi_object", fileName: file, mimeType: "mid")
        },
        to: postUrl, method: .post)
        .responseString(completionHandler: { (response) in
            
            if let err = response.error{
                completion(err.localizedDescription)
                return
            }
            completion("Succesfully uploaded")
            
        })
    }

    
    func getMIDI(_ completion: @escaping (String) -> ()) {
        let destination: DownloadRequest.Destination = { _, _ in
            let documentsURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            let fileURL = documentsURL.appendingPathComponent("test.mid")

            return (fileURL, [.removePreviousFile, .createIntermediateDirectories])
        }
        AF.download(getUrl, to: destination).validate().responseData(completionHandler: { response in
            guard let fileUrl = response.fileURL else {return print("failed to open file URL")}
            completion(fileUrl.lastPathComponent)
        })
    }
}

