// Header Section
// VHDL testbench threshold_TB
// Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen
// Reference: https://tinyurl.com/vicilogicVHDLTips 
// Component Name : threshold
// Title          : Generate a 32-x32-bit threshold array from 32x32-byte source data array
// Description    : refer to component hdl model fro function description and signal dictionary
// Author(s)      : Fearghal Morgan
// Company        : University of Galway
// Email          : fearghal.morgan@universityofgalway.ie
// Date           : 29/03/2023

module threshold_TB();

// testbench signal declarations
integer testNo; // aids locating test in simulation waveform
reg endOfSim; // assert at end of simulation to highlight simulation done. Stops clk signal generation.

// Typically use the same signal names as in the Verilog module
reg ce;
reg go;
reg [127:0] reg4x32_CSRA_128;
reg [127:0] reg4x32_CSRB_128;
reg [255:0] BRAM_dOut;

wire active;
wire wr;
wire [7:0] add;
wire [31:0] datToMem;
wire [95:0] functBus;

localparam period = 20; // 20 ns
localparam OneFifthPeriod = 4; // 4 ns

initial clk = 1'b1;
initial endOfSim = 1'b0;
 
// Generate clk signal, if sequential component, and endOfSim is 0.
always # (period/2.0) if (~endOfSim) clk = ~ clk;

threshold uut
	(
	.clk (clk), 
	.rst (rst),
	.ce (ce), 
	.go (go), 
	.reg4x32_CSRA_128 (reg4x32_CSRA_128), 
	.reg4x32_CSRB_128 (reg4x32_CSRB_128), 
	.BRAM_dOut (BRAM_dOut), 
	.active (active), 
	.wr (wr), 
	.add (add), 
	.datToMem (datToMem), 
	.functBus (functBus)
	);

initial
begin
    $timeformat(-9, 2, " ns", 20);
    $display("Simulation start :: time is %0t",$time);

	// Apply default input signal values. Do not assign output signals (generated by the UUT) here
	// Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge
	testNo = 0;
	rst    = 1'b1;
	ce = 1'b0;
	go = 1'b0;
	reg4x32_CSRA_128 = 128'h0;
	reg4x32_CSRB_128 = 128'h0;
	BRAM_dOut = 256'b0;
	#period 
	#OneFifthPeriod 
	rst   = 1'b0;
	repeat (2)
	 #period 

    $display("Assert and toggle rst",$time);
	rst = 1'b1;
    #period 
    #OneFifthPeriod 
    rst = 1'b0;
    #period 

// manually added code START
	// include testbench stimulus sequence here, i.e, input signal combinations and intervals (wait for n*period)
	// Use new testNo for each test set, to aid locating test on simulation waveform
	testNo <= 1;
// manually added code END

 // Print picosecond (ps) = 1000*ns (nanosecond) time to simulation transcript
 // Use to find time when simulation ends (endOfSim is TRUE)
 // Re-run the simulation for this time 
 // Select timing diagram and use View>Zoom Fit  
 $display("Simulation end :: time is %0t",$time);
 endOfSim = 1'b1; // assert to stop clk signal generation
end 
endmodule