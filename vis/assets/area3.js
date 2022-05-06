let data = [], width = 600, height = 400, numPoints = 100
let brush = d3.brush().on('start brush', handleBrush)

let brushExtent
function handleBrush(e) {
    brushExtent = e.selection
    update()
}

function handleMoveButton() {
    d3.select('svg').transition()
    .delay(50)
    .duration(500)
    .call(brush.move, [[50, 50], [150, 150]])
}

function handleClearButton() {
    d3.select('svg')
    .call(brush.clear)
}

function initBrush() {
    d3.select('svg').call(brush)
}

function updateData() {
    data = []
    for (let i=0; i < numPoints; i++) {
        data.push({
            id: i,
            x: Math.random() * width,
            y: Math.random() * height,
        })
    }
}

function isInBrushExtent(d) {
    return brushExtent &&
    d.x >= brushExtent[0][0] &&
    d.x <= brushExtent[1][0] &&
    d.y >= brushExtent[0][1] &&
    d.y <= brushExtent[1][1]
}

function update() {
    d3.select('svg')
    .selectAll('circle')
    .data(data)
    .join('circle')
    .attr('cx', function (d) {return d.x;})
    .attr('cy', function (d) {return d.y;})
    .attr('r', 4)
    .style('fill', function (d) {return isInBrushExtent(d) ? 'red' : 'black';})
}

initBrush()
updateData()
update()