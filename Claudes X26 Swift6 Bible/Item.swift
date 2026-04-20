//
//  Item.swift
//  Claudes X26 Swift6 Bible
//
//  Created by Michael Fluharty on 4/20/26.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
