// swift-tools-version: 5.9
import PackageDescription

/// Swift Package manifest for the Swiftora iOS application.
///
/// This manifest describes an iOS application built entirely from Swift
/// sources.  Dependencies are declared on GRDB for SQLite persistence
/// and Alamofire for simple networking.  You can open this package
/// directly in Xcode 15 or later to build and run the app on an iOS
/// simulator without needing a separate Xcode project file.
let package = Package(
    name: "Swiftora",
    defaultLocalization: "en",
    platforms: [
        .iOS(.v15)
    ],
    products: [
        .iOSApplication(
            name: "Swiftora",
            targets: ["AppModule"],
            bundleIdentifier: "com.eric.swiftora",
            teamIdentifier: "",
            displayVersion: "0.0.1",
            bundleVersion: "1",
            appIcon: .asset("swiftora_icon_1024"),
            accentColor: .named("AccentColor"),
            supportedDeviceFamilies: [ .phone ],
            supportedInterfaceOrientations: [ .portrait ]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/groue/GRDB.swift", from: "6.0.0"),
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.7.0")
    ],
    targets: [
        .executableTarget(
            name: "AppModule",
            dependencies: [
                .product(name: "GRDB", package: "GRDB.swift"),
                .product(name: "Alamofire", package: "Alamofire")
            ],
            path: "Sources"
        ),
        .testTarget(
            name: "SwiftoraTests",
            dependencies: ["AppModule"],
            path: "Tests"
        )
    ]
)