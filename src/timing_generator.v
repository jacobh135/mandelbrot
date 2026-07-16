module timing_generator (
    input wire clk, rst_n,
    output wire hsync, vsync, video_active,
    output reg [9:0] x_pos, y_pos
);

    always @(posedge clk) begin
        if (~rst_n) begin
            x_pos <= 0;
            y_pos <= 0;
        end
        else begin
            if (x_pos == 799) begin
                x_pos <= 0;
                if (y_pos == 524) begin
                    y_pos <= 0;
                end
                else begin
                    y_pos <= y_pos + 1;
                end
            end
            else begin
                x_pos <= x_pos + 1;
            end
        end
    end

    assign hsync = !((656 <= x_pos) && (751 >= x_pos));
    assign vsync = !((490 <= y_pos) && (491 >= y_pos));
    assign video_active = (639 >= x_pos) && (479 >= y_pos);

endmodule