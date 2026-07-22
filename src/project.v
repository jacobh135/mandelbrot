/*
 * Copyright (c) 2024 Jacob He
 * SPDX-License-Identifier: Apache-2.0
 */
 
`include "config.vh"

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
  wire cranker_done, time_enable, cranker_enable, count_advance, count_capture, hsync, vsync, video_active;
  wire signed [10:0] x_t, y_t;
  wire [9:0] x_pos, y_pos;
  wire signed [`FRAC+2:0] c_x, c_y;
  wire [4:0] count, active_count;
  wire [1:0] red, green, blue;

  control_unit c_unit(.cranker_done(cranker_done), .x_t(x_t), .y_t(y_t), .time_enable(time_enable), .cranker_enable(cranker_enable), .count_advance(count_advance), .count_capture(count_capture));
  timing_generator t_gen(.enable(time_enable), .clk(clk), .rst_n(rst_n), .hsync(hsync), .vsync(vsync), .video_active(video_active), .x_t(x_t), .y_t(y_t));
  pixel_generator px_gen(.x_t(x_t), .y_t(y_t), .x_pos(x_pos), .y_pos(y_pos));
  coordinate_mapper coor_map(.x_pos(x_pos), .y_pos(y_pos), .c_x(c_x), .c_y(c_y));
  cranker c(.enable(cranker_enable), .clk(clk), .rst_n(rst_n), .c_x(c_x), .c_y(c_y), .cranker_done(cranker_done), .count(count));
  count_register c_reg(.capture(count_capture), .advance(count_advance), .clk(clk), .rst_n(rst_n), .count(count), .active_count(active_count));
  colormap c_map(.active_count(active_count), .red(red), .green(green), .blue(blue));
  out_generator o_gen(.red(red), .green(green), .blue(blue), .hsync(hsync), .vsync(vsync), .video_active(video_active), .uo_out(uo_out));


  // // All output pins must be assigned. If not used, assign to 0.
  // assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in, uio_in, 1'b0};

endmodule
