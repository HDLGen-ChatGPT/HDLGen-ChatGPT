// Header Section
// VHDL testbench ADD2_TB
// Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen
// Reference: https://tinyurl.com/vicilogicVHDLTips 
// Component Name : ADD2
// Title          : 2-bit binary adder
// Description    : refer to component hdl model fro function description and signal dictionary
// Author(s)      : Fearghal Morgan
// Company        : University of Galway
// Email          : fearghal.morgan@universityofgalway.ie
// Date           : 29/03/2023

module ADD2_TB();

// testbench signal declarations
integer testNo; // aids locating test in simulation waveform
reg endOfSim; // assert at end of simulation to highlight simuation done. Stops clk signal generation.

// Typically use the same signal names as in the Verilog module

reg [1:0] addIn1;
reg [1:0] addIn0;
wire sum;

parameter  period = 20; // 20 ns

initial endOfSim = 1'b0;

//integer state [0:31];
integer i, j;
 
ADD2 uut
	(
	.addIn1 (addIn1), 
	.addIn0 (addIn0), 
	.sum (sum)
	);

initial
begin
 $timeformat(-9, 2, " ns", 20);
 $display("Simulation start :: time is %0t",$time);

	// Apply default INPUT signal values. Do not assign output signals (generated by the UUT) here
	// Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge
	testNo <= 0;
	addIn1 = 2'b00;
	addIn0 = 2'b00;
	repeat (2)
	 #20

// manually added code START
   // include testbench stimulus sequence here. USe new testNo for each test set
   // Use new testNo for each test set 
   // individual tests. Generate input signal combinations and wait for period.

    testNo <= 1; // use loop
    begin
      i = 0;
      j = 0;
      while (i < 4)
      begin
          addIn1 = i;
          j = 0;
          while (j < 4)
          begin
             addIn0 = j;
             #20
             j = j + 1;
          end
          i = i + 1;
      end 
    end 
    
    testNo <= 2; // apply individual signal stimuli 
	addIn1 = 2'b00;
	addIn0 = 2'b00;
    #20
	addIn0 = 2'b01;
	#20
	addIn0 = 2'b10;
	#20
	addIn0 = 2'b11;
	#20

	addIn1 = 2'b01;
	addIn0 = 2'b00;
    #20
	addIn0 = 2'b01;
	#20
	addIn0 = 2'b10;
	#20
	addIn0 = 2'b11;
	#20
	
	addIn1 = 2'b10;
	addIn0 = 2'b00;
    #20
	addIn0 = 2'b01;
	#20
	addIn0 = 2'b10;
	#20
	addIn0 = 2'b11;
	#20
	
	addIn1 = 2'b11;
	addIn0 = 2'b00;
    #20
	addIn0 = 2'b01;
	#20
	addIn0 = 2'b10;
	#20
	addIn0 = 2'b11;
	#20

	addIn1 = 2'b00;
	addIn0 = 2'b00;
 // manually added code END


 // Print picosecond (ps) = 1000*ns (nanosecond) time to simulation transcript
 // Use to find time when simulation ends (endOfSim is TRUE)
 // Re-run the simulation for this time 
 // Select timing diagram and use View>Zoom Fit  
 $display("Simulation end :: time is %0t",$time);
 endOfSim = 1'b1; // assert to stop clk signal generation

end

endmodule