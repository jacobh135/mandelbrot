`include "config.vh"

module coordinate_mapper #(parameter DW = `FRAC + 3) (
    input wire [9:0] x_pos, y_pos,
    output wire signed [DW-1:0] c_x, c_y
);
    localparam XSCALE = (7 * (1 << (`FRAC - 1)) + 319) / 639;
    localparam YSCALE = ((1 << (`FRAC + 1)) + 239) / 479;
    localparam XOFF = 5 << (`FRAC - 1);
    localparam YOFF = 1 << `FRAC;

    wire signed [DW-1:0] x_product, y_product;

    assign x_product = ($signed({1'b0, x_pos}) * XSCALE);
    assign y_product = ($signed({1'b0, y_pos}) * YSCALE);

    assign c_x = x_product - XOFF;
    assign c_y = y_product - YOFF;

endmodule