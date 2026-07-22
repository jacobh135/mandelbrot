`include "config.vh"

module cranker #(parameter DW = `FRAC + 3) (
    input wire enable, clk, rst_n,
    input wire signed [DW-1:0] c_x, c_y,
    output reg cranker_done,
    output reg [4:0] count
);
    localparam PW = 2 * DW;
    localparam CW = PW + 1;
    localparam signed [CW-1:0] ESCAPE = 64'd1 << (2 * `FRAC + 2);

    reg [4:0] state;
    reg signed [DW-1:0] z_x, z_y, c_x_s, c_y_s;
    wire signed [PW-1:0] z_x_2, z_y_2, z_y_z_x;

    assign z_x_2 = z_x * z_x;
    assign z_y_2 = z_y * z_y;
    assign z_y_z_x = z_x * z_y;

    always @(posedge clk) begin
        if (~rst_n) begin
            state <= 0;
            z_x <= 0;
            z_y <= 0;
            c_x_s <= 0;
            c_y_s <= 0;
            count <= 0;
            cranker_done <= 0;
        end
        else begin
            case (state)
                0: begin
                    if (enable) begin
                        state <= state + 1;
                        z_x <= z_x_2[`FRAC +: DW] - z_y_2[`FRAC +: DW] + c_x;
                        z_y <= z_y_z_x[`FRAC +: DW] + z_y_z_x[`FRAC +: DW] + c_y;
                        c_x_s <= c_x;
                        c_y_s <= c_y;
                    end
                    else begin
                        state <= state;
                    end
                    count <= 0;
                    cranker_done <= 0;
                end
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22: begin
                    if (z_x_2 + z_y_2 > ESCAPE) begin
                        state <= 0;
                        z_x <= 0;
                        z_y <= 0;
                        c_x_s <= 0;
                        c_y_s <= 0;
                        count <= state;
                        cranker_done <= 1;
                    end
                    else begin
                        state <= state + 1;
                        z_x <= z_x_2[`FRAC +: DW] - z_y_2[`FRAC +: DW] + c_x_s;
                        z_y <= z_y_z_x[`FRAC +: DW] + z_y_z_x[`FRAC +: DW] + c_y_s;
                    end
                end
                23: begin
                    if (z_x_2 + z_y_2 > ESCAPE) begin
                        count <= state;
                    end
                    else begin
                        count <= state + 1;
                    end
                    state <= 0;
                    z_x <= 0;
                    z_y <= 0;
                    c_x_s <= 0;
                    c_y_s <= 0;
                    cranker_done <= 1;
                end
            endcase
        end
    end

endmodule