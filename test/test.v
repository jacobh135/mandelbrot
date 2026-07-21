`default_nettype none
`timescale 1ns / 1ps

module test;
  initial begin
    $dumpfile(`DUMP_FILE);
    $dumpvars(0, `DUMP_TOP);
  end
endmodule