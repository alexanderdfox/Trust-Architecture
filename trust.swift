import Foundation

class Agent {
	var x: Double
	var y: Double
	var team: String  // 'fork' or 'zero'
	var children: [Agent] = []
	var infected: Bool = false
	var lastSpawn: TimeInterval
	var authenticated: Bool

	init(x: Double, y: Double, team: String) {
		self.x = x
		self.y = y
		self.team = team
		self.authenticated = team == "fork"
		self.lastSpawn = Date().timeIntervalSince1970
	}

	func update() {
		let now = Date().timeIntervalSince1970
		if infected {
			for child in children {
				if !child.infected {
					child.infected = true
				}
			}
		}

		if now - lastSpawn > 0.3 {  // Faster spawn rate
			spawnChildren()
			lastSpawn = now
		}
	}

	func spawnChildren() {
		if children.count >= 3 {
			return
		}
		for _ in 0..<2 {
			let angle = Double.random(in: 0..<2 * .pi)
			let dist = Double.random(in: 20..<50)
			let newX = x + cos(angle) * dist
			let newY = y + sin(angle) * dist
			var child: Agent?
			if team == "zero" {
				if Double.random(in: 0..<1) < 0.8 {
					child = Agent(x: newX, y: newY, team: "zero")
					child?.authenticated = true
				}
			} else {
				child = Agent(x: newX, y: newY, team: "fork")
			}
			if let child = child {
				children.append(child)
			}
		}
	}
}

var agents: [Agent] = []
let forkRoot = Agent(x: 200, y: 300, team: "fork")
let zeroRoot = Agent(x: 800, y: 300, team: "zero")
zeroRoot.authenticated = true
agents.append(forkRoot)
agents.append(zeroRoot)

var infectTime = Date().timeIntervalSince1970 + 3  // Infection starts after 3 seconds
var infected = false
var startTime = Date().timeIntervalSince1970
var forkCounts: [Int] = []
var zeroCounts: [Int] = []
var forkInfected: [Int] = []
var zeroInfected: [Int] = []
var timeSeries: [Int] = []

// Simulate for 15 seconds
while Date().timeIntervalSince1970 - startTime < 15 {
	// Infection logic
	if !infected && Date().timeIntervalSince1970 > infectTime {
		forkRoot.infected = true
		zeroRoot.infected = true
		infected = true
	}

	// Update agents and record counts
	for agent in agents {
		agent.update()
	}

	let forkTotal = agents.filter { $0.team == "fork" }.count
	let zeroTotal = agents.filter { $0.team == "zero" }.count
	let forkInf = agents.filter { $0.team == "fork" && $0.infected }.count
	let zeroInf = agents.filter { $0.team == "zero" && $0.infected }.count

	forkCounts.append(forkTotal)
	zeroCounts.append(zeroTotal)
	forkInfected.append(forkInf)
	zeroInfected.append(zeroInf)
	timeSeries.append(Int(Date().timeIntervalSince1970 - startTime))

	// Sleep for a short time to simulate real-time (speed can be adjusted)
	usleep(50000)  // Sleep for 50 milliseconds (adjust for speed)
}

// Output results as a basic simulation log
print("Fork Bomb Trust vs Zero Trust - Final Results:")
for t in 0..<forkCounts.count {
	print("Time: \(timeSeries[t])s - Fork Total: \(forkCounts[t]) - Fork Infected: \(forkInfected[t]) | Zero Total: \(zeroCounts[t]) - Zero Infected: \(zeroInfected[t])")
}

// Optional: You could also use Swift's plotting libraries like SwiftPlot or other methods to graph results