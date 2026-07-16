/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_jacobh135_mandelbrot (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  wire hsync, vsync, video_active;
  wire [1:0] red, green, blue;
  wire [9:0] x_pos, y_pos;

  timing_generator t_gen (.clk(clk), .rst_n(rst_n), .hsync(hsync), .vsync(vsync), .video_active(video_active), .x_pos(x_pos), .y_pos(y_pos));
  pattern_generator p_gen (.video_active(video_active), .x_pos(x_pos), .red(red), .green(green), .blue(blue));
  out_generator o_gen (.red(red), .green(green), .blue(blue),.hsync(hsync), .vsync(vsync), .video_active(video_active), .uo_out(uo_out));

  // // All output pins must be assigned. If not used, assign to 0.
  // assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in, uio_in, y_pos, 1'b0};

endmodule
